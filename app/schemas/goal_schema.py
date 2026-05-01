from pydantic import BaseModel
from typing import List

class GoalSchema(BaseModel):
    goal_title: str
    timeline: str
    current_background: str
    experience_level: str

    needs_clarification: bool
    clarification_questions: List[str]