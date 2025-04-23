from typing import List, Optional
from datetime import datetime, timedelta
from neurons.miner.models.event import MinerEvent
from neurons.validator.utils.logger.logger import InfiniteGamesLogger
from neurons.miner.services.if_games_service import IfGamesService
from neurons.miner.forecasters.rlhf_forecaster import RLHFForecaster

class EventService:
    def __init__(
        self,
        if_games_service: IfGamesService,
        logger: InfiniteGamesLogger,
        feedback_weight: float = 0.3
    ):
        self.if_games_service = if_games_service
        self.logger = logger
        self.feedback_weight = feedback_weight
        self.events: List[MinerEvent] = []

    async def refresh_events(self) -> List[MinerEvent]:
        try:
            # Get events from last 7 days
            from_date = int((datetime.now() - timedelta(days=7)).timestamp())
            self.logger.info(f"Refreshing events from date {from_date}")
            
            # Get events from service (will use mock if no real events)
            self.events = await self.if_games_service.get_events(from_date=from_date)
            self.logger.info(f"Received {len(self.events)} events from service")
            
            if not self.events:
                self.logger.warning("No events found, using mock events")
                self.events = await self.if_games_service.get_events(from_date=0)
                self.logger.info(f"Using {len(self.events)} mock events")
            
            # Update probabilities using RLHF forecaster
            self.logger.info("Updating probabilities with RLHF forecaster")
            for event in self.events:
                forecaster = RLHFForecaster(
                    event=event,
                    logger=self.logger,
                    if_games_client=self.if_games_service.client,
                    extremize=True,
                    feedback_weight=self.feedback_weight,
                    min_feedback_count=3,
                    use_feedback=True
                )
                event.probability = await forecaster._run()
            
            self.logger.info(f"Returning {len(self.events)} events with updated probabilities")
            return self.events
        except Exception as e:
            self.logger.error(f"Error refreshing events: {e}")
            # Return mock events as fallback
            mock_events = await self.if_games_service.get_events(from_date=0)
            self.logger.info(f"Using {len(mock_events)} mock events as fallback")
            return mock_events

    async def get_event(self, event_id: str) -> Optional[MinerEvent]:
        return next((event for event in self.events if event.event_id == event_id), None)

    async def process_feedback(
        self,
        event_id: str,
        agrees: bool,
        comment: Optional[str] = None
    ) -> bool:
        try:
            self.logger.info(f"Starting feedback process for event {event_id}")
            
            # Get the event
            event = await self.get_event(event_id)
            if not event:
                self.logger.error(f"Event {event_id} not found")
                return False
                
            self.logger.info(f"Found event: {event.event_id}")

            # Initialize RLHF forecaster
            self.logger.info("Initializing RLHF forecaster")
            forecaster = RLHFForecaster(
                event=event,
                logger=self.logger,
                if_games_client=self.if_games_service.client,
                extremize=True,
                feedback_weight=self.feedback_weight,
                min_feedback_count=3,
                use_feedback=True
            )

            # Add feedback using RLHF forecaster
            self.logger.info(f"Adding feedback: agrees={agrees}, comment={comment}")
            try:
                await forecaster.add_feedback(
                    event_id=event_id,
                    agrees=agrees,
                    comment=comment
                )
                self.logger.info("Feedback added successfully")
            except Exception as e:
                self.logger.error(f"Error adding feedback: {e}")
                return False

            # Update probability using RLHF
            self.logger.info("Updating probability with RLHF")
            try:
                new_probability = await forecaster._run()
                event.probability = new_probability
                self.logger.info(f"Probability updated to: {new_probability}")
            except Exception as e:
                self.logger.error(f"Error updating probability: {e}")
                return False
            
            self.logger.info("Feedback process completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in feedback process: {e}", exc_info=True)
            return False 