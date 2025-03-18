from fastapi import APIRouter, HTTPException, Depends
from services.auth_service import get_current_user
from models import AnswerSubmission, AnswerResponse
from services.answer_service import submit_answer

router = APIRouter()

@router.post("/api/interview/answer", response_model=AnswerResponse)
async def submit_interview_answer(answer_data: AnswerSubmission,  user: dict = Depends(get_current_user)):
    """
    Submit an answer and receive feedback.
    """
    response = submit_answer(answer_data.session_id, answer_data.question_id, answer_data.answer)

    if response is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return response