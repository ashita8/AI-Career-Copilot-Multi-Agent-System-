from fastapi import APIRouter
from uuid import uuid4
from app.graph.builder import graph
from app.schemas.request import ChatRequest,ResumeChatRequest
from fastapi.responses import StreamingResponse
from langgraph.types import Command
from app.agents.supervisor import general_chat_agent
import json

router = APIRouter()

@router.post("/chat/stream")
async def chat_stream(payload: ChatRequest):

    async def event_generator():

        thread_id = payload.thread_id or str(uuid.uuid4())

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        yield f"data: {json.dumps({'type':'meta','thread_id':thread_id})}\n\n"

        for chunk in graph.stream(
            {
                "message": payload.message,
                "resume_text": payload.resume_text
            },
            config=config
        ):
            yield f"data: {json.dumps({'type':'chunk','data':chunk})}\n\n"

        yield f"data: {json.dumps({'type':'done'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


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