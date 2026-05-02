# app/schemas/resume_schema.py

from pydantic import BaseModel
from typing import List


class ResumeSchema(BaseModel):
    resume_score: str
    missing_sections: List[str]
    missing_keywords: List[str]
    weak_bullets: List[str]
    rewritten_summary: str
    top_projects_to_add: List[str]
    ats_tips: List[str]
    final_verdict: str