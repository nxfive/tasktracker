from fastapi import APIRouter, Depends, status, HTTPException
from app.auth.oauth2 import get_current_user
from database.setup import get_db
from sqlalchemy.orm import Session
from schemas.user import UserDisplay, UserUpdate, UserCreate, UserBase
from crud.user import crud_user
from typing import Annotated, List

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserDisplay])
def get_all_users(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    return crud_user.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserDisplay)
def create_user(
    request: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    check_username = crud_user.get_by_username(db, username=request.username)
    if check_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken",
        )
    check_email = crud_user.get_by_email(db, email=request.email)
    if check_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email address is already associated with an account",
        )
    return crud_user.create(db, request)


@router.get("/{user_id}", response_model=UserDisplay)
def get_user_by_id(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    user = crud_user.get_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/{username}", response_model=UserDisplay)
def get_user_by_username(
    username: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, get_current_user],
):
    user = crud_user.get_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.patch("/update/{user_id}")
def update_user(
    user_id: int,
    request: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    user = crud_user.get_by_id(db, user_id=user_id)
    if not user or user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return crud_user.update(db, request, user_id=user_id)


@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    user = crud_user.get_by_id(db, user_id=user_id)
    if not user or user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return crud_user.delete(db, user_id=user_id)
