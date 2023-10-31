from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Annotated
from schemas.task import TaskDisplay, TaskUpdate, TaskCreate
from schemas.user import UserBase
from sqlalchemy.orm import Session
from database.setup import get_db
from crud.task import crud_task
from app.auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/", response_model=List[TaskDisplay])
def get_all_tasks(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    return crud_task.get_all(db, user_id=current_user.id)


@router.get("/{task_id}", response_model=TaskDisplay)
def get_task_by_id(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    task = crud_task.get_by_id(db, task_id=task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskDisplay)
def create_task(
    request: TaskCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    return crud_task.create(db, request, user_id=current_user.id)


@router.patch(
    "/update/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskDisplay
)
def update_task(
    task_id: int,
    request: TaskUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    task = crud_task.get_by_id(db, task_id=task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return crud_task.update(db, request, task_id=task.id, user_id=current_user.id)


@router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    task = crud_task.get_by_id(db, task_id=task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return crud_task.delete(db, task)
