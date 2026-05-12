from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.database import get_db
from models.domain import OutfitFeedback

router = APIRouter(prefix="/api/feedback", tags=["feedback"])

class FeedbackRequest(BaseModel):
    outfit_details: str
    liked: bool
    weather_context: str = None

@router.post("/")
def submit_feedback(feedback: FeedbackRequest, db: Session = Depends(get_db)):
    db_feedback = OutfitFeedback(
        suggested_items_ids=feedback.outfit_details,
        liked=feedback.liked,
        weather_context=feedback.weather_context
    )
    db.add(db_feedback)
    db.commit()
    
    # Here you could trigger a background task to update user preference embeddings
    
    return {"message": "Feedback recorded"}
