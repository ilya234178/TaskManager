# Task Manager API

Backend API built with FastAPI.

## Requirements
- Python 3.10+

## Setup & Run (Windows)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

This project uses PostgreSQL database: task_manager