from fastapi import APIRouter, HTTPException, Depends
from services.auth_service import get_current_user
from models import InterviewEndRequest, InterviewSummaryResponse
from services.interview_service import end_interview_session

router = APIRouter()


@router.post("/api/interview/end", response_model=InterviewSummaryResponse)
async def end_interview(request: InterviewEndRequest, user: dict = Depends(get_current_user)):
    """
    End an interview session and generate summary feedback.
    """
    summary = end_interview_session(request.session_id)

    if summary is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return summary