import os
import uuid
from database import interview_recording_collection

# Define storage directory
STORAGE_DIR = "recordings/"
os.makedirs(STORAGE_DIR, exist_ok=True)

def start_recording(session_id: str):
    """
    Initializes a new recording for an interview session.
    """
    recording_id = str(uuid.uuid4())
    storage_path = f"{STORAGE_DIR}{recording_id}.webm"

    interview_recording_collection.insert_one({"recording_id": recording_id, "session_id": session_id, "storage_path": storage_path})
    return {"recording_id": recording_id, "storage_path": storage_path}

def upload_recording_chunk(session_id: str, chunk_number: int, chunk_data: bytes):
    """
    Stores a chunk of recorded video/audio.
    """
    recording = interview_recording_collection.find_one({"session_id": session_id})
    if not recording:
        return None

    file_path = recording["storage_path"]
    with open(file_path, "ab") as f:  # Append binary data
        f.write(chunk_data)

    return True

def end_recording(session_id: str, recording_id: str):
    """
    Finalizes the recording and returns the stored path.
    """
    recording = interview_recording_collection.find_one({"recording_id": recording_id, "session_id": session_id})
    if not recording:
        return None

    return {"recording_url": recording["storage_path"]}