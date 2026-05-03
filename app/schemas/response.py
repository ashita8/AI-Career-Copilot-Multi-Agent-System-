from pydantic import BaseModel
from typing import Any, List, Optional


class UISection(BaseModel):
    type: str
    title: str
    data: Any


class ChatResponse(BaseModel):
    thread_id: str
    agent: str
    message: str
    sections: List[UISection] = []
    raw_state: Optional[dict] = None