from fastapi import APIRouter
from uuid import uuid4
from app.graph.builder import graph
from app.schemas.request import ChatRequest,ResumeChatRequest
from langgraph.types import Command
from app.agents.supervisor import general_chat_agent

router = APIRouter()

@router.post("/chat")
async def chat(payload: ChatRequest):
    thread_id = str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = graph.invoke(
    {
        "message": payload.message,
        "query": payload.message
    },
    config=config
    )
    return {
        "thread_id": thread_id,
        "result": result
    }


@router.post("/chat/resume")
async def resume_chat(payload: ResumeChatRequest):

    config = {
        "configurable": {
            "thread_id": payload.thread_id
        }
    }

    result = graph.invoke(
        Command(resume=payload.message),
        config=config
    )

    return result