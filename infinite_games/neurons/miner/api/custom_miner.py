from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from neurons.miner.services.event_service import EventService
from neurons.miner.services.if_games_service import IfGamesService
from neurons.validator.if_games.client import IfGamesClient
from neurons.validator.utils.logger.logger import InfiniteGamesLogger
from neurons.miner.config import MinerConfig

router = APIRouter()
logger = InfiniteGamesLogger(name="custom_miner_api")

# Initialize config and services
config = MinerConfig(
    env="test",
    network="test",
    netuid=155
)
if_games_client = IfGamesClient(
    env=config.env,
    logger=logger,
    bt_wallet=config.wallet
)
if_games_service = IfGamesService(client=if_games_client, logger=logger)
event_service = EventService(
    if_games_service=if_games_service,
    logger=logger,
    feedback_weight=config.feedback_weight
)

class EventResponse(BaseModel):
    event_id: str
    market_type: str
    probability: float
    description: str
    cutoff: datetime
    status: str

class FeedbackRequest(BaseModel):
    event_id: str
    agrees: bool
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    success: bool
    message: str
    timestamp: datetime

@router.get("/events", response_model=List[EventResponse])
async def get_events():
    try:
        logger.info("Fetching events from event service")
        events = await event_service.refresh_events()
        logger.info(f"Retrieved {len(events)} events from service")
        
        if not events:
            logger.warning("No events found, using mock events")
            # Get mock events directly from IfGamesService with default from_date
            events = await if_games_service.get_events(from_date=0)
            logger.info(f"Retrieved {len(events)} mock events")
        
        response = [
            EventResponse(
                event_id=event.event_id,
                market_type=event.market_type,
                probability=event.probability,
                description=event.description,
                cutoff=event.cutoff,
                status=event.status.serialize()
            )
            for event in events
        ]
        
        logger.info(f"Successfully formatted {len(response)} events for response")
        return response
    except Exception as e:
        logger.error(f"Error in get_events endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching events: {str(e)}"
        )

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackRequest):
    try:
        # First verify the event exists
        events = await if_games_client.get_events(from_date=0, offset=0, limit=100)
        event_exists = any(event.event_id == feedback.event_id for event in events)
        
        if not event_exists:
            logger.warning(f"Event {feedback.event_id} not found")
            raise HTTPException(status_code=404, detail="Event not found")
            
        # Submit feedback
        result = await if_games_client.post_feedback(
            event_id=feedback.event_id,
            agrees=feedback.agrees,
            comment=feedback.comment
        )
        
        return FeedbackResponse(
            success=True,
            message="Feedback submitted successfully",
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))