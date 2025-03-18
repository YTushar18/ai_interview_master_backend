from pydantic import BaseModel, EmailStr
from typing import List, Optional

class User(BaseModel):
    name: str
    email: EmailStr
    password: str  # Will be hashed before storing


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    user_id: str
    access_token: str


class InterviewHistory(BaseModel):
    user_id: str
    timestamp: str
    job_role: str
    difficulty: str
    score: Optional[float]


class InterviewSession(BaseModel):
    user_id: str
    job_role: str
    difficulty: str
    timestamp: str
    questions: List[str]
    session_id: Optional[str] = None


class InterviewMetadata(BaseModel):
    session_id: str
    user_id: str
    job_role: str
    difficulty: str
    timestamp: str


class AnswerSubmission(BaseModel):
    session_id: str
    question_id: int
    answer: str


class AnswerResponse(BaseModel):
    feedback: str
    next_question: Optional[str]


class InterviewEndRequest(BaseModel):
    session_id: str


class InterviewSummaryResponse(BaseModel):
    summary: str
    score: float
    feedback: str


class UserProfileResponse(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    bio: Optional[str] = None
    job_title: Optional[str] = None
    skills: Optional[list] = None


class UpdateUserProfileRequest(BaseModel):
    user_id: str
    name: Optional[str] = None
    bio: Optional[str] = None
    job_title: Optional[str] = None
    skills: Optional[list] = None


class StartRecordingRequest(BaseModel):
    session_id: str


class StartRecordingResponse(BaseModel):
    recording_id: str
    storage_path: str


class UploadRecordingChunkRequest(BaseModel):
    session_id: str
    chunk_number: int


class EndRecordingRequest(BaseModel):
    session_id: str
    recording_id: str


class FeedbackRequest(BaseModel):
    session_id: str
    question_id: int
    answer: str


class FeedbackResponse(BaseModel):
    feedback: str
    improvement_areas: list
    score: float