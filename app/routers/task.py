from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Annotated
from app.schemas.task import TaskDisplay, TaskUpdate, TaskCreate
from app.schemas.user import UserBase
from sqlalchemy.orm import Session
from app.database.setup import get_db
from app.crud.task import crud_task
from app.auth.oauth2 import get_current_user
from app.exceptions.custom import EntityNotExist

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/", response_model=List[TaskDisplay])
def get_all_tasks(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    return crud_task.get_all(db, attr_name="user_id", id=current_user.id)


@router.get("/{task_id}", response_model=TaskDisplay)
def get_task_by_id(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    task = crud_task.get_by_id(db, id=task_id)
    if not task or task.user_id != current_user.id:
        raise EntityNotExist(entity="task")
    return task


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskDisplay)
def create_task(
    request: TaskCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    return crud_task.create(db, request, user_id=current_user.id)


@router.patch(
    "/{task_id}/update", status_code=status.HTTP_200_OK, response_model=TaskDisplay
)
def update_task(
    task_id: int,
    request: TaskUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    task = crud_task.get_by_id(db, id=task_id)
    if not task or task.user_id != current_user.id:
        raise EntityNotExist(entity="task")
    return crud_task.update(db, request, task_id=task.id, user_id=current_user.id)


@router.delete("/{task_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    task = crud_task.get_by_id(db, id=task_id)
    if not task or task.user_id != current_user.id:
        raise EntityNotExist(entity="task")
    return crud_task.delete(db, task)
