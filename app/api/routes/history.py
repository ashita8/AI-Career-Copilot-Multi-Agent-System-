from fastapi import APIRouter

from app.db.database import SessionLocal
from app.db.crud import list_conversations, get_messages

router = APIRouter(prefix="/history", tags=["History"])


# -----------------------------------
# GET ALL CHATS (Sidebar)
# -----------------------------------
@router.get("/")
async def get_all_chats():

    db = SessionLocal()

    try:
        rows = list_conversations(db)

        return {
            "conversations": [
                {
                    "thread_id": row.thread_id,
                    "title": row.title,
                    "updated_at": row.updated_at
                }
                for row in rows
            ]
        }

    finally:
        db.close()


# -----------------------------------
# GET SINGLE CHAT HISTORY
# -----------------------------------
@router.get("/{thread_id}")
async def get_chat(thread_id: str):

    db = SessionLocal()

    try:
        rows = get_messages(db, thread_id)

        return {
            "thread_id": thread_id,
            "messages": [
                {
                    "role": row.role,
                    "content": row.content,
                    "created_at": row.created_at
                }
                for row in rows
            ]
        }

    finally:
        db.close()