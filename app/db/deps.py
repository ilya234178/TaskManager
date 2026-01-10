from typing import Generator

from app.db.session import Sessionlocal
from sqlalchemy.orm import Session


def get_db() -> Generator[Session, None, None]:
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()