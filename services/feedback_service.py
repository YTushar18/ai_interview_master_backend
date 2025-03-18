import random

def generate_feedback(answer: str):
    """
    Generates basic AI feedback for an answer.
    """
    # Placeholder AI logic (Later replace with LLM model)
    length = len(answer)
    keywords = ["clarity", "depth", "examples", "confidence"]
    improvement_areas = []

    if length < 10:
        improvement_areas.append("Your answer is too short. Elaborate more.")
    if length > 10 and "example" not in answer.lower():
        improvement_areas.append("Consider providing an example for better clarity.")
    if "um" in answer.lower() or "uh" in answer.lower():
        improvement_areas.append("Avoid using filler words like 'um' or 'uh'.")

    score = min(100, max(40, length * 2))  # Normalize to 100 max
    return {
        "feedback": "Your response was good, but it can be improved!" if score > 60 else "Try improving your response.",
        "improvement_areas": improvement_areas,
        "score": round(score, 2)
    }