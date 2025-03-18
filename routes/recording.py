from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from services.auth_service import get_current_user
from models import StartRecordingRequest, StartRecordingResponse, UploadRecordingChunkRequest, EndRecordingRequest
from services.recording_service import start_recording, upload_recording_chunk, end_recording

router = APIRouter()

@router.post("/api/interview/recording/start", response_model=StartRecordingResponse)
async def start_interview_recording(request: StartRecordingRequest, user: dict = Depends(get_current_user)):
    """
    Initialize recording for an interview session.
    """
    response = start_recording(request.session_id)
    return response

@router.post("/api/interview/recording/chunk")
async def upload_interview_recording_chunk(session_id: str, chunk_number: int, file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    """
    Upload a chunk of recorded video/audio.
    """
    chunk_data = await file.read()
    success = upload_recording_chunk(session_id, chunk_number, chunk_data)

    if not success:
        raise HTTPException(status_code=404, detail="Recording session not found")

    return {"message": f"Chunk {chunk_number} uploaded successfully"}

@router.post("/api/interview/recording/end")
async def end_interview_recording(request: EndRecordingRequest, user: dict = Depends(get_current_user)):
    """
    Finalize recording and return stored recording URL.
    """
    response = end_recording(request.session_id, request.recording_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Recording not found")

    return response