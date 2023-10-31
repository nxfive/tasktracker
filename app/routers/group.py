from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated
from app.database.setup import get_db
from sqlalchemy.orm import Session
from app.schemas.user import UserBase
from app.schemas.group import GroupUpdate, GroupCreate, GroupDisplay
from app.crud.group import crud_group
from app.auth.oauth2 import get_current_user


router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/", response_model=List[GroupDisplay])
def get_all_groups(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    return crud_group.get_all_groups(db, user_id=current_user.id)


@router.get("/{group_id}", response_model=GroupDisplay)
def get_group_by_id(
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    group = crud_group.get_by_id(db, group_id=group_id)
    if not group and group.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group not found"
        )
    return group


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GroupDisplay)
def create_group(
    request: GroupCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    return crud_group.create(db, request, user_id=current_user.id)


@router.patch("/update/{group_id}", response_model=GroupDisplay)
def update_group(
    group_id: int,
    request: GroupUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    group = crud_group.get_by_id(db, group_id=group_id)
    if not group or group.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group not found"
        )
    return crud_group.update(db, request, user_id=current_user.id, group_id=group_id)


@router.delete("/delete/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    group = crud_group.get_by_id(db, group_id=group_id)
    if not group or group.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group not found"
        )
    return crud_group.delete(db, group)
