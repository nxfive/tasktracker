from fastapi import APIRouter, Depends
from typing import Annotated
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas.admin import AdminDisplay, AdminUserDisplay, AdminCreate, AdminUpdate
from typing import List
from app.crud import crud_admin


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.get("/", response_model=List[AdminDisplay])
def get_all_admins(db: Annotated[Session, Depends(get_db)]):
    return crud_admin.get_all_admins(db)


@router.post("/", response_model=AdminDisplay)
def create_admin(db: Annotated[Session, Depends(get_db)],
                 request: AdminCreate):
    return crud_admin.create_admin(db, request)


@router.patch("/access/{user_id}")
def assign_admin(user_id: int, db: Annotated[Session, Depends(get_db)]):
    return crud_admin.assign(db, user_id=user_id)


@router.get("/users", response_model=List[AdminUserDisplay])
def get_all_users(db: Annotated[Session, Depends(get_db)]):
    return crud_admin.get_all_users(db)


@router.post("/me/{admin_id}/update", response_model=AdminDisplay)
def update(admin_id: int,
           db: Annotated[Session, Depends(get_db)],
           request: AdminUpdate):
    return crud_admin.update(db, request, admin_id=admin_id)
