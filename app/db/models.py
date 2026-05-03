from sqlalchemy import Column, String, Text, DateTime, Integer
from datetime import datetime
from db.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    thread_id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=True)
    state_json = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)

    thread_id = Column(String, index=True)
    role = Column(String)       # user / assistant
    content = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)