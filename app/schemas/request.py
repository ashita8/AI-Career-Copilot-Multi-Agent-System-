

from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str


class ResumeChatRequest(BaseModel):
    thread_id: str
    message: str