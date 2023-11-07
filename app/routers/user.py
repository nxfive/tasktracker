from fastapi import APIRouter, Depends, status, HTTPException
from app.auth.oauth2 import get_current_user
from app.database.setup import get_db
from sqlalchemy.orm import Session
from app.schemas.user import UserDisplay, UserUpdate, UserCreate, UserBase
from app.crud.user import crud_user
from typing import Annotated, List
from app.exceptions.custom import EntityNotExist
import logging


router = APIRouter(prefix="/users", tags=["users"])

logger = logging.getLogger(__name__)


@router.get("/", response_model=List[UserDisplay])
def get_all_users(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    return crud_user.get_all(db)


# @router.get("/{user_id}", response_model=UserDisplay)
# def get_user_by_id(
#     user_id: int,
#     db: Annotated[Session, Depends(get_db)],
#     current_user: Annotated[UserBase, Depends(get_current_user)],
# ):
#     user = crud_user.get_by_id(db, id=user_id)
#     if not user:
#         raise EntityNotExist(entity="user")
#     return user


@router.get("/{username}", response_model=UserDisplay)
def get_user_by_username(
    username: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    user = crud_user.get_by_attr(db, attr_name="username", value=username)
    if not user:
        raise EntityNotExist(entity="user")
    return user


@router.get("/{email}", response_model=UserDisplay)
def get_user_by_email(
    email: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    user = crud_user.get_by_attr(db, attr_name="email", value=email)
    if not user:
        raise EntityNotExist(entity="user")
    return user


@router.patch("/{user_id}/update")
def update_user(
    user_id: int,
    request: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    user = crud_user.get_by_id(db, id=user_id)
    if not user or user.id != current_user.id:
        raise EntityNotExist(entity="user")
    return crud_user.update(db, request, user_id=user_id)


@router.delete("/{user_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    user = crud_user.get_by_id(db, id=user_id)
    if not user or user.id != current_user.id:
        raise EntityNotExist(entity="user")
    return crud_user.delete(db, user_id=user_id)
