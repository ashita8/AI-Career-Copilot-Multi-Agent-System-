from typing import TypedDict, Dict, Any

class CareerState(TypedDict, total=False):
    message: str
    query: str   # optional backward compatibility
    resume_text: str

    goal_data: dict
    jd_data: list[str]
    skill_gap_data: dict
    roadmap_data: dict
    project_data: dict
    resume_data: dict
    general_chat_data: dict

    needs_clarification: bool
    clarification_questions: list[str]
    user_answers: dict