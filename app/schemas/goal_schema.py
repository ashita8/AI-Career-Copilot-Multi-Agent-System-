from pydantic import BaseModel
from typing import Optional, List

class GoalSchema(BaseModel):
    goal_title: str
    timeline: Optional[str] = None
    current_background: Optional[str] = None
    experience_level: Optional[str] = None

    needs_clarification: bool = False
    missing_fields: List[str] = []
    clarification_questions: List[str] = []


class FollowupSchema(BaseModel):
    timeline: Optional[str]
    current_background: Optional[str]
    experience_level: Optional[str]