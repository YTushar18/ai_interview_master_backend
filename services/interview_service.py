import random
import uuid
from database import interview_sesssions_collection
from datetime import datetime
from database import db

# Define question sets
QUESTIONS_DB = {
    "Software Engineer": {
        "Easy": [
            "What is object-oriented programming?",
            "Explain the difference between HTTP and HTTPS.",
            "What is a linked list?"
        ],
        "Medium": [
            "How does a hash table work?",
            "Explain the time complexity of quicksort.",
            "What is the difference between REST and GraphQL?"
        ],
        "Hard": [
            "How does a distributed system handle consistency?",
            "Explain CAP theorem in detail.",
            "How does garbage collection work in Java?"
        ]
    },
    "Data Scientist": {
        "Easy": [
            "What is linear regression?",
            "Explain the concept of overfitting.",
            "What is a confusion matrix?"
        ],
        "Medium": [
            "What are precision, recall, and F1-score?",
            "How do you handle missing values in a dataset?",
            "Explain PCA and its use cases."
        ],
        "Hard": [
            "Explain variational autoencoders and their applications.",
            "How do GANs work?",
            "What is the role of backpropagation in deep learning?"
        ]
    },
    "frontend-developer": {
      "easy": [
        "Can you explain the difference between let, const, and var in JavaScript?",
        "What is the DOM and how do you interact with it?",
        "Explain the box model in CSS.",
        "What is responsive design and how do you implement it?",
        "Describe the difference between inline and block elements.",
      ],
      "medium": [
        "Explain how React's virtual DOM works and its benefits.",
        "What are closures in JavaScript and how would you use them?",
        "Describe the difference between controlled and uncontrolled components in React.",
        "How do you handle state management in large React applications?",
        "Explain CSS specificity and the cascade.",
      ],
      "hard": [
        "Explain how you would implement a custom hook in React and when you would use it.",
        "Describe your approach to performance optimization in React applications.",
        "How would you implement code-splitting in a React application?",
        "Explain how you would set up a CI/CD pipeline for a frontend project.",
        "Describe your experience with micro-frontend architecture.",
      ],
    },
    "backend-developer": {
      "easy": [
        "What is RESTful API design?",
        "Explain the difference between SQL and NoSQL databases.",
        "What is middleware in the context of web servers?",
        "Describe the HTTP request/response cycle.",
        "What is the purpose of environment variables?",
      ],
      "medium": [
        "Explain database indexing and when you would use it.",
        "How do you handle authentication and authorization in a web application?",
        "Describe your approach to error handling in a backend application.",
        "What are the ACID properties in database transactions?",
        "Explain the concept of microservices architecture.",
      ],
      "hard": [
        "How would you design a system that needs to handle high throughput?",
        "Explain your approach to database sharding and partitioning.",
        "Describe how you would implement a rate limiting system.",
        "How would you design a distributed caching system?",
        "Explain your experience with event-driven architecture.",
      ],
    }
}

def generate_questions(job_role: str, difficulty: str):
    """
    Generate interview questions based on job role and difficulty level.
    """
    return random.sample(QUESTIONS_DB.get(job_role, {}).get(difficulty, []), 3)

def store_interview_metadata(session_id: str, user_id: str, job_role: str, difficulty: str, timestamp: str):
    """
    Stores interview session metadata in the database.
    """
    metadata = {
        "session_id": session_id,
        "user_id": user_id,
        "job_role": job_role,
        "difficulty": difficulty,
        "timestamp": timestamp
    }
    db["interview_metadata"].insert_one(metadata)

def start_interview_session(user_id: str, job_role: str, difficulty: str):
    """
    Starts a new interview session.
    """
    session_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    questions = generate_questions(job_role, difficulty)

    session_data = {
        "session_id": session_id,
        "user_id": user_id,
        "job_role": job_role,
        "difficulty": difficulty,
        "timestamp": timestamp,
        "questions": questions
    }

    # Store session in MongoDB
    interview_sesssions_collection.insert_one(session_data)

    # Store metadata separately
    store_interview_metadata(session_id, user_id, job_role, difficulty, timestamp)

    return session_data


def calculate_score(session_id: str):
    """
    Calculates a score for the interview session.
    """
    answers = list(db["interview_answers"].find({"session_id": session_id}))
    if not answers:
        return 0.0

    total_score = sum(len(ans["answer"]) for ans in answers)  # Example: Score based on answer length
    avg_score = total_score / len(answers) if answers else 0.0
    return min(100, avg_score)  # Normalize to 100 max



def end_interview_session(session_id: str):
    """
    Marks an interview session as completed.
    """
    session = db["interview_sessions"].find_one({"session_id": session_id})
    if not session:
        return None

    score = calculate_score(session_id)
    feedback = "Great job! Keep practicing." if score > 50 else "Consider improving your explanations."

    summary = {
        "session_id": session_id,
        "summary": "Interview completed successfully.",
        "score": score,
        "feedback": feedback
    }

    db["interview_summaries"].insert_one(summary)
    return summary