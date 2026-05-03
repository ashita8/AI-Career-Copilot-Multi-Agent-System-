

from typing import Optional

from pydantic import BaseModel,Field

class ChatRequest(BaseModel):
    thread_id: Optional[str] = None
    message: str
    resume_text: Optional[str] = None


class ResumeChatRequest(BaseModel):
    thread_id: str = Field(
        example="thread-123"
    )
    message: str = Field(
        example="I want to become a GenAI Engineer"
    )