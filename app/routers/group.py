from fastapi import APIRouter, Depends, status
from typing import List, Annotated
from app.database.setup import get_db
from sqlalchemy.orm import Session
from app.schemas.user import UserBase, UserGet
from app.schemas.group import GroupUpdate, GroupCreate, GroupDisplay
from app.crud.group import crud_group
from app.auth.oauth2 import get_current_user
from app.services.group import add_user, delete_user
from app.exceptions.custom import EntityNotExist, PermissionDenied

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
    group = crud_group.get_by_id(db, id=group_id)
    if not group and group.owner_id != current_user.id:
        raise EntityNotExist(entity="group")
    return group


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GroupDisplay)
def create_group(
    request: GroupCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    return crud_group.create(db, request, user_id=current_user.id)


@router.patch("/{group_id}/update", response_model=GroupDisplay)
def update_group(
    group_id: int,
    request: GroupUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    group = crud_group.get_by_id(db, id=group_id)
    if not group or group.owner_id != current_user.id:
        raise EntityNotExist(entity="group")

    return crud_group.update(db, request, group)


@router.delete("/{group_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    group = crud_group.get_by_id(db, id=group_id)
    if not group or group.owner_id != current_user.id:
        raise EntityNotExist(entity="group")
    return crud_group.delete(db, group)


@router.post("{group_id}/admins/add")
def add_admin(
    group_id: int,
    request: UserGet,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    group = crud_group.get_by_id(db, id=group_id)
    if not group:
        raise EntityNotExist(entity="group")
    if group.owner_id != current_user.id:
        raise PermissionDenied
    return add_user(db, request, group, admin=True)


@router.post("{group_id}/admins/delete")
def delete_admin(
    group_id: str,
    request: UserGet,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    group = crud_group.get_by_id(db, id=group_id)
    if not group:
        raise EntityNotExist(entity="group")
    if group.owner_id != current_user.id:
        raise PermissionDenied
    return add_user(db, request, group, admin=True)


@router.post("{group_id}/members/add")
def add_member(
    group_id: str,
    request: UserGet,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    group = crud_group.get_by_id(db, id=group_id)
    if not group:
        raise EntityNotExist(entity="group")
    if group.owner_id != current_user.id or current_user.id not in [
        user.id for user in group.admins
    ]:
        raise PermissionDenied
    return add_user(db, request, group, admin=False)


@router.post("{group_id}/members/delete")
def delete_member(
    group_id: str,
    request: UserGet,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    group = crud_group.get_by_id(db, id=group_id)
    if not group:
        raise EntityNotExist(entity="group")
    if group.owner_id != current_user.id:
        raise PermissionDenied
    return delete_user(db, request, group, admin=False)
