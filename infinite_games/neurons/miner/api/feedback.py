from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from neurons.miner.forecasters.rlhf_forecaster import RLHFForecaster
from neurons.validator.utils.logger.logger import InfiniteGamesLogger

router = APIRouter()

class FeedbackRequest(BaseModel):
    event_id: str
    agrees: bool
    comment: Optional[str] = None
    user_id: Optional[str] = None
    user_reputation: Optional[float] = None

class FeedbackResponse(BaseModel):
    success: bool
    message: str
    timestamp: datetime

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    feedback: FeedbackRequest,
    forecaster: RLHFForecaster,
    logger: InfiniteGamesLogger
):
    try:
        forecaster.add_feedback(
            event_id=feedback.event_id,
            agrees=feedback.agrees,
            comment=feedback.comment,
            user_id=feedback.user_id,
            user_reputation=feedback.user_reputation
        )
        
        return FeedbackResponse(
            success=True,
            message="Feedback submitted successfully",
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 