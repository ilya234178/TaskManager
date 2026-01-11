from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password, verify_password

def list_users(db: Session) -> list[User]:
    return db.query(User).all()

def create_user(db: Session, email: str) -> User:
    user = User(email=email)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Дубликат email")
    
    db.refresh(user)
    return user 

def delete_user(db: Session, user_id: int) -> None:
    user = db.get(User, user_id)
    if user is None:
        raise ValueError("not_found")

    db.delete(user)
    db.commit()

def update_user(db: Session, user_id: int, email: str) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise ValueError("not_found")
    
    if email is not None:
        user.email = email

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("duplicate_email")
    
    db.refresh(user)
    return user

def register_user(db: Session, email: str, password: str) -> User:
    user = User(email=email, password_hash=hash_password(password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("duplicate_email")
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise ValueError("invalid_credentials")
    if not verify_password(password, user.password_hash):
        raise ValueError("invalid_credentials")
    return user