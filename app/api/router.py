from fastapi import APIRouter
from app.api.routes import health,users, tasks

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(users.router)
api_router.include_router(tasks.router)
