from pydantic import BaseModel
from typing import List, Dict


class ProjectSchema(BaseModel):
    beginner_projects: List[str]
    intermediate_projects: List[str]
    advanced_projects: List[str]

    must_have_portfolio_project: Dict[str, str]

    github_strategy: List[str]