from pydantic import BaseModel
from typing import List


class RoadmapSchema(BaseModel):
    phase_1: List[str]
    phase_2: List[str]
    phase_3: List[str]

    weekly_plan: List[str]

    milestones: List[str]

    daily_hours: str