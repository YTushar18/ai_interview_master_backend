from database import db

def generate_feedback(answer: str) -> str:
    """
    Generates basic feedback for an answer.
    (Later, replace this with AI-powered evaluation)
    """
    if len(answer) < 10:
        return "Your answer is too short, try to elaborate more."
    return "Good answer! Consider adding more technical details."

def submit_answer(session_id: str, question_id: int, answer: str):
    """
    Stores user answer and generates feedback.
    """
    session = db["interview_sessions"].find_one({"session_id": session_id})
    if not session:
        return None

    # Store answer
    answer_data = {
        "session_id": session_id,
        "question_id": question_id,
        "answer": answer,
        "feedback": generate_feedback(answer)
    }
    db["interview_answers"].insert_one(answer_data)

    # Fetch next question (if available)
    questions = session["questions"]
    next_question = questions[question_id + 1] if question_id + 1 < len(questions) else None

    return {
        "feedback": answer_data["feedback"],
        "next_question": next_question
    }