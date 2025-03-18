from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, interview, job, answers, end_interview, user, recording, feedback

app = FastAPI(
    title="AI-Powered Interview Coach API",
    description="This API powers an AI-driven mock interview platform with real-time feedback, session tracking, and media recording.",
    version="1.0.0"
)

# ✅ Allow Frontend Access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)

# Register Routes
app.include_router(auth.router)
app.include_router(interview.router)
app.include_router(job.router)
app.include_router(answers.router)
app.include_router(end_interview.router)
app.include_router(user.router)
app.include_router(recording.router)
app.include_router(feedback.router)

@app.get("/")
def read_root():
    return {"message": "AI Interview Coach API is running!"}