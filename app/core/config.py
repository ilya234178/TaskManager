import os
from dotenv import load_dotenv

load_dotenv()


APP_NAME = "Task Manager API"
API_V1_PREFIX = "/api/v1"

DATABASE_URL = (os.getenv("DATABASE_URL") or "").strip()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_me_in_env")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60