from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User

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