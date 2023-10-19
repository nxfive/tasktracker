from fastapi import APIRouter, Depends, status
from typing import List, Annotated
from schemas.task import TaskDisplay, TaskUpdate, TaskCreate
from schemas.user import UserBase
from sqlalchemy.orm import Session
from database.setup import get_db
from crud.task import crud_task
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[TaskDisplay])
def get_all_tasks(db: Annotated[Session, Depends(get_db)],
                  current_user: Annotated[UserBase, Depends(get_current_user)]):
    return crud_task.get_all_tasks(db, user_id=current_user.id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(request: TaskCreate,
                db: Annotated[Session, Depends(get_db)],
                current_user: Annotated[UserBase, Depends(get_current_user)]
                ):
    return crud_task.create_task(db, request, user_id=current_user.id)


@router.patch("/update/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: int, request: TaskUpdate,
                db: Annotated[Session, Depends(get_db)],
                current_user: Annotated[UserBase, Depends(get_current_user)]
                ):
    return crud_task.update_task(db, request, task_id=task_id, user_id=current_user.id)


@router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int,
                db: Annotated[Session, Depends(get_db)],
                current_user: Annotated[UserBase, Depends(get_current_user)]
                ):
    return crud_task.delete_task(db, task_id=task_id, user_id=current_user.id)
