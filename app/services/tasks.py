from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User


def list_tasks(db: Session, user_id: int | None = None) -> list[Task]:
    query = db.query(Task)
    if user_id is not None:
        query = query.filter(Task.user_id == user_id)
    return query.all()


def create_task(db: Session, title: str, user_id: int) -> Task:
    # проверяем, что пользователь существует
    user = db.get(User, user_id)
    if user is None:
        raise ValueError("user_not_found")

    task = Task(title=title, user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(
    db: Session,
    task_id: int,
    user_id: int,
    title: str | None = None,
    is_done: bool | None = None,
) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task is None:
        raise ValueError("not_found")

    if title is not None:
        task.title = title
    if is_done is not None:
        task.is_done = is_done

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user_id: int) -> None:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task is None:
        raise ValueError("not_found")

    db.delete(task)
    db.commit()
