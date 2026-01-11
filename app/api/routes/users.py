from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.deps import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services import users as user_service 

router = APIRouter(tags=["users"])

@router.get("/users", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return user_service.list_users(db)


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, email=payload.email)
    except ValueError as e:
        if str(e) == "duplicate_email":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
        raise


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user_service.delete_user(db, user_id=user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        if str(e) == "not_found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        raise 

@router.patch("/users/{user_id}", response_model=UserRead)
def patch_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    try:
        return user_service.update_user(db, user_id=user_id, email=payload.email)
    except ValueError as e:
        if str(e) == "not_found":
            raise HTTPException(status_code=404, detail="User not found")
        if str(e) == "duplicate_email":
            raise HTTPException(status_code=409, detail="User with this email already exists")
        raise