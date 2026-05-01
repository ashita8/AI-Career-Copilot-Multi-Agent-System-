from typing import TypedDict, Dict, Any

class CareerState(TypedDict, total=False):
    query: str
    goal_data: dict

    jd_data: list[str]
    skill_gap_data: dict
    roadmap_data: dict

    needs_clarification: bool
    clarification_questions: list[str]
    user_answers: dict
    