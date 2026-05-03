from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from uuid import uuid4
import json

from langgraph.types import Command

from graph.builder import graph
from schemas.request import ChatRequest, ResumeChatRequest

from db.database import SessionLocal
from db.crud import load_state, save_state, save_message

router = APIRouter()


# ==========================================================
# STREAMING CHAT
# ==========================================================
@router.post("/chat/stream")
async def chat_stream(payload: ChatRequest):

    async def event_generator():

        raw_thread_id = (payload.thread_id or "").strip()

        thread_id = (
            str(uuid4())
            if raw_thread_id in ["", "string", "null", "None"]
            else raw_thread_id
        )

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        yield f"data: {json.dumps({'type': 'meta', 'thread_id': thread_id})}\n\n"

        for chunk in graph.stream(
            {
                "message": payload.message,
                "resume_text": payload.resume_text
            },
            config=config
        ):
            yield f"data: {json.dumps({'type': 'chunk', 'data': chunk}, default=str)}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


# ==========================================================
# MAIN CHAT (Persistent + Interrupt Resume)
# ==========================================================
@router.post("/chat")
async def chat(payload: ChatRequest):

    db = SessionLocal()

    try:
        # -----------------------------------
        # Thread ID handling
        # -----------------------------------
        raw_thread_id = (payload.thread_id or "").strip()

        thread_id = (
            str(uuid4())
            if raw_thread_id in ["", "string", "null", "None"]
            else raw_thread_id
        )

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        # -----------------------------------
        # Save user message
        # -----------------------------------
        save_message(db, thread_id, "user", payload.message)

        # -----------------------------------
        # Load previous state
        # -----------------------------------
        previous_state = load_state(db, thread_id)

        # -----------------------------------
        # If waiting on interrupt -> resume flow
        # -----------------------------------
        if previous_state.get("pending_interrupt"):

            result = graph.invoke(
                Command(resume=payload.message),
                config=config
            )

        # -----------------------------------
        # Normal conversation
        # -----------------------------------
        else:

            state = {
                **previous_state,
                "message": payload.message,
                "resume_text": getattr(payload, "resume_text", None)
            }

            result = graph.invoke(
                state,
                config=config
            )

        # -----------------------------------
        # Track interrupt state
        # -----------------------------------
        if "__interrupt__" in result:
            result["pending_interrupt"] = True
        else:
            result["pending_interrupt"] = False

        # -----------------------------------
        # Save graph state
        # -----------------------------------
        save_state(db, thread_id, result)

        # -----------------------------------
        # Save assistant reply
        # -----------------------------------
        assistant_reply = extract_reply(result)

        save_message(
            db,
            thread_id,
            "assistant",
            assistant_reply
        )

        return {
            "thread_id": thread_id,
            "result": result
        }

    finally:
        db.close()


# ==========================================================
# LEGACY RESUME RESUME-COMMAND ENDPOINT
# ==========================================================
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


# ==========================================================
# HELPER: CLEAN ASSISTANT MESSAGE
# ==========================================================
def extract_reply(result: dict) -> str:

    if "general_chat_data" in result:
        return result["general_chat_data"].get("reply", "Response generated.")

    if "resume_data" in result:
        return "Resume analysis completed."

    if "roadmap_data" in result:
        return "Roadmap generated."

    if "project_data" in result:
        return "Project recommendations generated."

    if "__interrupt__" in result:
        interrupt = result["__interrupt__"][0]
        value = getattr(interrupt, "value", None)

        if isinstance(value, dict):
            return value.get("message", "Need more information.")

        return str(value or "Need more information.")

    return "Response generated."