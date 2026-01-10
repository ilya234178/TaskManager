from fastapi import FastAPI
from app.core.config import APP_NAME, API_V1_PREFIX
from app.api.router import api_router

from app.db.session import engine
from app.db.base import Base
from app.models import User  # важно: импорт, чтобы модель зарегистрировалась

Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME)
app.include_router(api_router, prefix=API_V1_PREFIX)