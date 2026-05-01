from pydantic import BaseModel
from typing import List

class SkillGapSchema(BaseModel):
    current_strengths: List[str]
    missing_skills: List[str]
    priority_skills: List[str]
    hiring_signals: List[str]
    readiness_level: str