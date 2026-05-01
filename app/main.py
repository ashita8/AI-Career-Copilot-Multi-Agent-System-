from fastapi import FastAPI
from app.api.router import api_router

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
    docs_url="/docs",         # Swagger UI
    redoc_url="/redoc",       # ReDoc
    openapi_url="/openapi.json"
)

app.include_router(api_router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "CareerForge API Running"}