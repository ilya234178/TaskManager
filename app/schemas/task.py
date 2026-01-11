from typing import Optional
from pydantic import BaseModel, ConfigDict

class TaskCreate(BaseModel):
    title: str
    user_id: int

class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    is_done: bool
    user_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    is_done: Optional[bool] = None