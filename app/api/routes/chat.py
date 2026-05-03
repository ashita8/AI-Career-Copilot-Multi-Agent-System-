from fastapi import APIRouter
from uuid import uuid4
from app.graph.builder import graph
from app.schemas.request import ChatRequest,ResumeChatRequest
from fastapi.responses import StreamingResponse
from langgraph.types import Command
from app.agents.supervisor import general_chat_agent

from app.db.database import SessionLocal
from app.db.crud import load_state, save_state

import json

router = APIRouter()

@router.post("/chat/stream")
async def chat_stream(payload: ChatRequest):

    async def event_generator():

        thread_id = payload.thread_id or str(uuid4())

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

    db = SessionLocal()

    try:
        raw_thread_id = (payload.thread_id or "").strip()

        if raw_thread_id in ["", "string", "null", "None"]:
            thread_id = str(uuid4())
        else:
            thread_id = raw_thread_id

        # Load old memory
        previous_state = load_state(db, thread_id)

        # Merge new message
        state = {
            **previous_state,
            "message": payload.message
        }

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        result = graph.invoke(state, config=config)

        # Save updated graph state
        save_state(db, thread_id, result)

        return {
            "thread_id": thread_id,
            "result": result
        }

    finally:
        db.close()

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