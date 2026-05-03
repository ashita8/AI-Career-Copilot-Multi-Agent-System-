from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import api_router
from db.database import engine, Base

# Import models so SQLAlchemy registers tables
from db import models

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CareerForge AI",
    description="""
Multi-Agent Career Copilot API built with FastAPI + LangGraph + Groq.

Features:
- AI Career Roadmaps
- Skill Gap Analysis
- Resume Review
- Streaming Chat Responses
- Multi-Agent Orchestration
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later restrict to localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "CareerForge API Running"}
