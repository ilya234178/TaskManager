from fastapi import APIRouter
from app.api.routes import health,users, tasks, auth

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(users.router)
api_router.include_router(tasks.router)
api_router.include_router(auth.router)
