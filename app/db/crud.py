import json
from datetime import datetime

from app.db.models import Conversation


# -----------------------------------
# Get Conversation Row
# -----------------------------------
def get_conversation(db, thread_id):
    return db.query(Conversation).filter(
        Conversation.thread_id == thread_id
    ).first()


# -----------------------------------
# Load Previous State
# -----------------------------------
def load_state(db, thread_id):

    convo = get_conversation(db, thread_id)

    if not convo:
        return {}

    if not convo.state_json:
        return {}

    try:
        return json.loads(convo.state_json)

    except Exception:
        return {}


# -----------------------------------
# Clean Non JSON Serializable Data
# -----------------------------------
def clean_state(data):

    if isinstance(data, dict):
        cleaned = {}

        for k, v in data.items():

            # remove internal graph keys
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
# Save Updated State
# -----------------------------------
def save_state(db, thread_id, state):

    convo = get_conversation(db, thread_id)

    safe_state = clean_state(state)

    payload = json.dumps(safe_state)

    if convo:
        convo.state_json = payload
        convo.updated_at = datetime.utcnow()

    else:
        convo = Conversation(
            thread_id=thread_id,
            state_json=payload
        )
        db.add(convo)

    db.commit()