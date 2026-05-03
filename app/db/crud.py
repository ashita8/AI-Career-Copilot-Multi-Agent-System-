import json
from datetime import datetime

from app.db.models import Conversation, Message


# -----------------------------------
# Get Conversation
# -----------------------------------
def get_conversation(db, thread_id):
    return db.query(Conversation).filter(
        Conversation.thread_id == thread_id
    ).first()


# -----------------------------------
# Save Message
# -----------------------------------
def save_message(db, thread_id, role, content):

    msg = Message(
        thread_id=thread_id,
        role=role,
        content=content
    )

    db.add(msg)
    db.commit()


# -----------------------------------
# Get Chat History
# -----------------------------------
def get_messages(db, thread_id):

    return db.query(Message).filter(
        Message.thread_id == thread_id
    ).order_by(Message.created_at.asc()).all()


# -----------------------------------
# Get All Conversations
# -----------------------------------
def list_conversations(db):

    return db.query(Conversation).order_by(
        Conversation.updated_at.desc()
    ).all()


# -----------------------------------
# Load State
# -----------------------------------
def load_state(db, thread_id):

    convo = get_conversation(db, thread_id)

    if not convo or not convo.state_json:
        return {}

    try:
        return json.loads(convo.state_json)

    except Exception:
        return {}


# -----------------------------------
# Clean State
# -----------------------------------
def clean_state(data):

    if isinstance(data, dict):

        cleaned = {}

        for k, v in data.items():

            if str(k).startswith("__"):
                continue

            cleaned[k] = clean_state(v)

        return cleaned

    elif isinstance(data, list):
        return [clean_state(x) for x in data]

    elif isinstance(data, (str, int, float, bool)) or data is None:
        return data

    return str(data)


# -----------------------------------
# Save State
# -----------------------------------
def save_state(db, thread_id, state):

    convo = get_conversation(db, thread_id)

    safe_state = clean_state(state)

    payload = json.dumps(safe_state)

    title = safe_state.get("message", "New Chat")[:60]

    if convo:
        convo.state_json = payload
        convo.updated_at = datetime.utcnow()

        if not convo.title:
            convo.title = title

    else:
        convo = Conversation(
            thread_id=thread_id,
            title=title,
            state_json=payload
        )

        db.add(convo)

    db.commit()