from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.deps import get_db
from app.core.security import  create_access_token
from app.schemas.auth import RegisterRequest, TokenResponse
from app.services import users as user_service

router = APIRouter(tags=["auth"])

@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = user_service.register_user(db, email=payload.email, password=payload.password)
        return{"id": user.id, "email": user.email}
    except ValueError as e:
        if str(e) == "duplicate_email":
            raise HTTPException(status_code=409, detail="User with this email already exists")
        raise
    
@router.post("/auth/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm ждёт form-data: username, password
    try:
        user = user_service.authenticate_user(db, email=form.username, password=form.password)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)

