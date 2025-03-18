from fastapi import APIRouter, Depends, HTTPException
from database import interview_history_collection, interview_metadata_collection
from services.interview_service import start_interview_session
from services.auth_service import get_current_user
from models import InterviewHistory, InterviewSession, InterviewMetadata
from bson import ObjectId
from typing import List

router = APIRouter()

@router.get("/api/interview/history", response_model=List[InterviewHistory])
async def get_interview_history(user: dict = Depends(get_current_user)):
    """
    Fetch interview history for a given user ID.
    """

    user_id = str(user["_id"])
    history = list(interview_history_collection.find({"user_id": user_id}))

    if not history:
        raise HTTPException(status_code=404, detail="No interview history found")

    # Convert ObjectId to string before returning
    for record in history:
        record["_id"] = str(record["_id"])

    return history



@router.post("/api/interview/start", response_model=InterviewSession)
async def start_interview(job_role: str, difficulty: str, user: dict = Depends(get_current_user)):
    """
    Start a new AI-based interview session.
    """
    if not job_role or not difficulty:
        raise HTTPException(status_code=400, detail="Job role and difficulty are required")

    user_id = str(user["_id"])
    session_data = start_interview_session(user_id, job_role, difficulty)
    return session_data


@router.get("/api/interview/metadata", response_model=List[InterviewMetadata])
async def get_interview_metadata(user: dict = Depends(get_current_user)):
    """
    Fetch stored interview metadata for a user.
    """

    user_id = str(user["_id"])
    metadata = list(interview_metadata_collection.find({"user_id": user_id}))

    if not metadata:
        raise HTTPException(status_code=404, detail="No interview metadata found")

    # Convert ObjectId to string
    for record in metadata:
        record["_id"] = str(record["_id"])

    return metadata