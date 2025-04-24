from typing import List, Optional
from datetime import datetime, timedelta
from neurons.miner.models.event import MinerEvent
from neurons.validator.utils.logger.logger import InfiniteGamesLogger
from neurons.miner.services.if_games_service import IfGamesService
from neurons.miner.forecasters.llm_forecaster import LLMForecaster

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
        self.prediction_history = {}  # Track prediction changes
        self.expert_performance = {}  # Track expert performance

    async def refresh_events(self) -> List[MinerEvent]:
        try:
            # Get events from last 7 days
            from_date = int((datetime.now() - timedelta(days=7)).timestamp())
            self.logger.info(f"Refreshing events from date {from_date}")
            
            # Get events from service (will use mock if no real events)
            events = await self.if_games_service.get_events(from_date=from_date)
            self.logger.info(f"Received {len(events)} events from service")
            
            if not events:
                self.logger.warning("No events found, using mock events")
                events = await self.if_games_service.get_events(from_date=0)
                self.logger.info(f"Using {len(events)} mock events")
            
            # Only update probabilities for real events, preserve mock event probabilities
            self.logger.info("Updating probabilities with LLM forecaster")
            for event in events:
                # Check if this is a mock event by looking at the event_id
                is_mock_event = any(event.event_id == mock_event.event_id for mock_event in get_mock_events())
                if not is_mock_event and not event.probability:
                    forecaster = LLMForecaster(
                        event=event,
                        logger=self.logger,
                        if_games_client=self.if_games_service.client,
                        extremize=True
                    )
                    event.probability = await forecaster._run()
            
            # Store events
            self.events = events
            
            self.logger.info(f"Returning {len(self.events)} events with updated probabilities")
            return self.events
        except Exception as e:
            self.logger.error(f"Error refreshing events: {e}")
            if not hasattr(self, 'events') or not self.events:
                mock_events = await self.if_games_service.get_events(from_date=0)
                self.events = mock_events
                self.logger.info(f"Using {len(mock_events)} mock events as fallback")
            return self.events

    async def get_event(self, event_id: str) -> Optional[MinerEvent]:
        """
        Get event by ID, refreshing events if not found
        """
        # Try to find event in current list
        event = next((event for event in self.events if event.event_id == event_id), None)
        
        # If not found, try refreshing events
        if not event:
            self.logger.info(f"Event {event_id} not found, refreshing events")
            await self.refresh_events()
            event = next((event for event in self.events if event.event_id == event_id), None)
            
        if not event:
            self.logger.warning(f"Event {event_id} not found after refresh")
            
        return event

    async def process_feedback(
        self,
        event_id: str,
        agrees: bool,
        expert_weight: float = 1.0,
        expert_id: str = None
    ):
        try:
            self.logger.info(f"Processing feedback for event {event_id} from expert {expert_id}")
            
            event = await self.get_event(event_id)
            if not event:
                self.logger.error(f"Event {event_id} not found in service")
                return False
            
            old_probability = event.probability
            self.logger.info(f"Current probability for event {event_id}: {old_probability}")
            
            forecaster = LLMForecaster(
                event=event,
                logger=self.logger,
                if_games_client=self.if_games_service.client,
                extremize=True
            )
            
            new_prediction = await forecaster.adjust_with_feedback(
                current_prediction=old_probability,
                agrees=agrees,
                expert_weight=expert_weight,
                expert_id=expert_id,
                event_id=event_id
            )
            
            self.logger.info(f"New prediction for event {event_id}: {new_prediction}")
            
            # Record prediction change
            if event_id not in self.prediction_history:
                self.prediction_history[event_id] = []
            self.prediction_history[event_id].append({
                "timestamp": datetime.now(),
                "old_probability": old_probability,
                "new_probability": new_prediction,
                "expert_id": expert_id,
                "expert_weight": expert_weight,
                "agrees": agrees
            })
            
            # Update expert performance
            if expert_id not in self.expert_performance:
                self.expert_performance[expert_id] = {
                    "total_feedbacks": 0,
                    "successful_feedbacks": 0
                }
            self.expert_performance[expert_id]["total_feedbacks"] += 1
            
            event.probability = new_prediction
            
            try:
                await self.if_games_service.client.post_predictions({
                    event_id: {"probability": new_prediction}
                })
                self.logger.info(f"Successfully posted new prediction for event {event_id}")
                return True
            except Exception as e:
                self.logger.error(f"Error posting prediction to validators: {e}")
                return False
            
        except Exception as e:
            self.logger.error(f"Error processing feedback: {e}", exc_info=True)
            return False 