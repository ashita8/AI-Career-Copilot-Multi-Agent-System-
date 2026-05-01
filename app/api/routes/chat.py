from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Chat"])

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(payload: ChatRequest):
    return {
        "query": payload.message,
        "response": "Career advice generated here"
    }