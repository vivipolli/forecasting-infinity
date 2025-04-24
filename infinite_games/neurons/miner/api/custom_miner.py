from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json

from neurons.miner.services.event_service import EventService
from neurons.miner.services.if_games_service import IfGamesService
from neurons.validator.if_games.client import IfGamesClient
from neurons.validator.utils.logger.logger import InfiniteGamesLogger
from neurons.miner.config import MinerConfig
from neurons.miner.models.event import MinerEvent

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
    expert_weight: float = 1.0  # Default weight for experts
    expert_id: str  # Required expert identifier

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
            
            # Store events in service for future feedback
            event_service.events = events
        
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
        logger.info(f"Received feedback request: {feedback}")
        
        # First try to get real events
        logger.info("Attempting to get real events from if_games_client")
        events = await if_games_client.get_events(from_date=0, offset=0, limit=100)
        logger.info(f"Received {len(events) if events else 0} real events")
        
        # If no real events, get mock events
        if not events:
            logger.info("No real events found, getting mock events from if_games_service")
            events = await if_games_service.get_events(from_date=0)
            logger.info(f"Received {len(events) if events else 0} mock events")
        
        # Convert events to MinerEvent objects
        miner_events = []
        for event in events:
            try:
                # If event is already a MinerEvent, use it directly
                if isinstance(event, MinerEvent):
                    miner_events.append(event)
                    continue
                    
                # If event is a dict, convert it to MinerEvent
                if isinstance(event, dict):
                    miner_events.append(MinerEvent(
                        event_id=event.get('event_id', event.get('id', '')),
                        market_type=event.get('market_type', 'BINARY'),
                        probability=event.get('probability', 0.5),
                        description=event.get('description', ''),
                        cutoff=event.get('cutoff', datetime.now()),
                        status=event.get('status', 'UNRESOLVED')
                    ))
                else:
                    logger.warning(f"Unexpected event type: {type(event)}")
                    # If it's a string, try to parse it as JSON
                    if isinstance(event, str):
                        try:
                            event_dict = json.loads(event)
                            miner_events.append(MinerEvent(
                                event_id=event_dict.get('event_id', event_dict.get('id', '')),
                                market_type=event_dict.get('market_type', 'BINARY'),
                                probability=event_dict.get('probability', 0.5),
                                description=event_dict.get('description', ''),
                                cutoff=event_dict.get('cutoff', datetime.now()),
                                status=event_dict.get('status', 'UNRESOLVED')
                            ))
                        except json.JSONDecodeError:
                            logger.error(f"Failed to parse event string as JSON: {event}")
            except Exception as e:
                logger.error(f"Error converting event: {str(e)}")
                continue
        
        logger.info(f"Total events after conversion: {len(miner_events)}")
        logger.info(f"Event IDs: {[event.event_id for event in miner_events]}")
        
        event_exists = any(event.event_id == feedback.event_id for event in miner_events)
        
        if not event_exists:
            logger.warning(f"Event {feedback.event_id} not found in either real or mock events")
            raise HTTPException(status_code=404, detail="Event not found")
            
        # Process feedback with expert weight and ID
        logger.info(f"Processing feedback for event {feedback.event_id} from expert {feedback.expert_id}")
        success = await event_service.process_feedback(
            event_id=feedback.event_id,
            agrees=feedback.agrees,
            expert_weight=feedback.expert_weight,
            expert_id=feedback.expert_id
        )
        
        if not success:
            logger.error(f"Failed to process feedback for event {feedback.event_id}")
            raise HTTPException(
                status_code=500,
                detail="Failed to process feedback"
            )
        
        logger.info(f"Successfully processed feedback for event {feedback.event_id}")
        return FeedbackResponse(
            success=True,
            message="Feedback processed successfully",
            timestamp=datetime.now()
        )
    except HTTPException as e:
        logger.error(f"HTTP error submitting feedback: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))