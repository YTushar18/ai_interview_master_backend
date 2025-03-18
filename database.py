from pymongo import MongoClient

# MongoDB Connection URL (Modify if needed)
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "interview_coach"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Collections

# Stores job interview questions
interview_history_collection = db["interview_history"]

# --
interview_metadata_collection = db["interview_metadata"]

# Stores interview sessions
interview_sesssions_collection = db["interview_sessions"]

# Stores user profiles
users_collection = db["users"]

# Stores interview questions and answers
interview_answers_collection = db["interview_answers"]

# Stores recording metadata (session_id, recording_id, storage_path)
interview_recording_collection  = db["recordings"]