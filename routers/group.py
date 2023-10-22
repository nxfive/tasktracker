from fastapi import APIRouter, Depends
from typing import List, Annotated
from database.setup import get_db
from sqlalchemy.orm import Session
from schemas.user import UserBase
from schemas.group import GroupUpdate, GroupCreate, GroupDisplay
from crud.group import crud_group
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix="/groups",
    tags=["groups"]
)


@router.get("/", response_model=List[GroupDisplay])
def get_all_groups(db: Annotated[Session, Depends(get_db)],
                   current_user: Annotated[UserBase, Depends(get_current_user)]):
    if current_user:
        return crud_group.get_all_groups(db, user_id=current_user.id)


@router.post("/")
def create_group(request: GroupCreate,
                 db: Annotated[Session, Depends(get_db)],
                 current_user: Annotated[UserBase, Depends(get_current_user)]):
    return crud_group.create(db, request, user_id=current_user.id)


@router.patch("/update/{group_id}", response_model=GroupDisplay)
def update_group(group_id: int,
                 request: GroupUpdate,
                 db: Annotated[Session, Depends(get_db)],
                 current_user: Annotated[UserBase, Depends(get_current_user)]):
    return crud_group.update(db, request, group_id=group_id, user_id=current_user.id)


@router.delete("/delete/{group_id}")
def delete_group(group_id: int,
                 db: Annotated[Session, Depends(get_db)],
                 current_user: Annotated[UserBase, Depends(get_current_user)]):
    return crud_group.delete(db, group_id=group_id, user_id=current_user.id)
