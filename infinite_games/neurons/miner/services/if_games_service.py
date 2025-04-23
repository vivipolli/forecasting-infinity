from typing import List, Optional
from neurons.validator.if_games.client import IfGamesClient
from neurons.validator.utils.logger.logger import InfiniteGamesLogger
from neurons.miner.models.event import MinerEvent
from neurons.miner.mocks.events import get_mock_events

class IfGamesService:
    def __init__(self, client: IfGamesClient, logger: InfiniteGamesLogger):
        self.client = client
        self.logger = logger
        self.feedback_history = {}  # Store feedback history

    async def get_events(self, from_date: int = 0) -> List[MinerEvent]:
        try:
            self.logger.info(f"Attempting to get events from date {from_date}")
            
            # Try to get real events first
            events = await self.client.get_events(from_date=from_date)
            self.logger.info(f"Received {len(events) if events else 0} real events")
            
            if not events:
                self.logger.warning("No real events found, using mock events for demo")
                events = get_mock_events()
                self.logger.info(f"Using {len(events)} mock events")
            
            return events
        except Exception as e:
            self.logger.error(f"Error getting events: {e}")
            # Fallback to mock events for demo
            mock_events = get_mock_events()
            self.logger.info(f"Using {len(mock_events)} mock events as fallback")
            return mock_events

    async def submit_feedback(
        self,
        event_id: str,
        agrees: bool,
        comment: Optional[str] = None
    ) -> bool:
        try:
            # Initialize feedback history for this event if not exists
            if event_id not in self.feedback_history:
                self.feedback_history[event_id] = {
                    "agrees": 0,
                    "disagrees": 0,
                    "total": 0
                }
            
            # Update feedback counts
            if agrees:
                self.feedback_history[event_id]["agrees"] += 1
            else:
                self.feedback_history[event_id]["disagrees"] += 1
            self.feedback_history[event_id]["total"] += 1
            
            self.logger.info(
                f"Feedback submitted for event {event_id}: "
                f"agrees={agrees}, comment={comment}, "
                f"total feedbacks={self.feedback_history[event_id]['total']}"
            )
            
            return True
        except Exception as e:
            self.logger.error(f"Error submitting feedback: {e}")
            return False

    def get_feedback_weight(self, event_id: str) -> float:
        """Calculate feedback weight based on agreement ratio"""
        if event_id not in self.feedback_history:
            return 0.5  # Neutral weight if no feedback
            
        history = self.feedback_history[event_id]
        if history["total"] == 0:
            return 0.5
            
        # Calculate agreement ratio (0 to 1)
        agreement_ratio = history["agrees"] / history["total"]
        return agreement_ratio 