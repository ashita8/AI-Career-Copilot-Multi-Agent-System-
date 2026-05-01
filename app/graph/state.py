from typing import TypedDict, Dict, Any

class CareerState(TypedDict, total=False):
    query: str
    goal_data: dict
    needs_clarification: bool
    clarification_questions: list[str]
    user_answers: dict