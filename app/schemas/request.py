

from typing import Optional

from pydantic import BaseModel

class ChatRequest(BaseModel):
    thread_id: Optional[str] = None
    message: str
    resume_text: Optional[str] = None


class ResumeChatRequest(BaseModel):
    thread_id: str
    message: str