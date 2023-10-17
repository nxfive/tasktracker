from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from typing import List
from schemas.user import UserDisplay, UserUpdate, UserCreate
from database.setup import get_db
from crud.user import crud_user

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return crud_user.get_all_users(db)


@router.post("/create")
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, request)


@router.get("/{username}", response_model=UserDisplay)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    return crud_user.get_user_by_username(db, username=username)


@router.patch("/update/{user_id}")
def update_user(user_id: int, request: UserUpdate, db: Session = Depends(get_db)):
    return crud_user.update_user(db, request, user_id=user_id)


@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud_user.delete_user(db, user_id=user_id)
