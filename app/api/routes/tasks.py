from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services import tasks as task_service
from app.api.deps.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["tasks"])


@router.get("/tasks", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return task_service.list_tasks(db, user_id=current_user.id)

@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return task_service.create_task(db, title=payload.title, user_id=current_user.id)


@router.patch("/tasks/{task_id}", response_model=TaskRead)
def patch_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return task_service.update_task(
            db,
            task_id=task_id,
            user_id=current_user.id,
            title=payload.title,
            is_done=payload.is_done,
        )
    except ValueError as e:
        if str(e) == "not_found":
            raise HTTPException(status_code=404, detail="Task not found")
        raise


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        task_service.delete_task(db, task_id=task_id, user_id=current_user.id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        if str(e) == "not_found":
            raise HTTPException(status_code=404, detail="Task not found")
        raise


