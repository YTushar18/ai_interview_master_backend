from fastapi import APIRouter, Depends
from models import FeedbackRequest, FeedbackResponse
from services.auth_service import get_current_user
from services.feedback_service import generate_feedback

router = APIRouter()

@router.post("/api/feedback/generate", response_model=FeedbackResponse)
async def generate_interview_feedback(request: FeedbackRequest, user: dict = Depends(get_current_user)):
    """
    Generates AI-powered feedback on an interview response.
    """
    feedback_data = generate_feedback(request.answer)
    return feedback_data