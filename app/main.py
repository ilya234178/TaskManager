from fastapi import FastAPI
from app.core.config import APP_NAME, API_V1_PREFIX
from app.api.router import api_router

app = FastAPI(title=APP_NAME)
app.include_router(api_router, prefix=API_V1_PREFIX)