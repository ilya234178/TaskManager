import os
from dotenv import load_dotenv

load_dotenv()


APP_NAME = "Task Manager API"
API_V1_PREFIX = "/api/v1"

DATABASE_URL = (os.getenv("DATABASE_URL") or "").strip()