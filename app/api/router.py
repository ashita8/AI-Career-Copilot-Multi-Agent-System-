from fastapi import APIRouter
from api.routes.chat import router as chat_router
from api.routes.health import router as health_router
from api.routes.resume import router as resume_router
from api.routes.history import router as history_router

api_router = APIRouter(prefix="/api")

api_router.include_router(chat_router)
api_router.include_router(health_router)
api_router.include_router(resume_router)
api_router.include_router(history_router)