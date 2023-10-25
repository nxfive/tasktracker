from fastapi import APIRouter, Depends
from typing import Annotated
from database.setup import get_db
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user
from schemas.user import UserBase
from schemas.label import LabelDisplay, LabelUpdate, LabelCreate
from crud.label import crud_label
from typing import List

router = APIRouter(
    prefix="/labels",
    tags=["labels"]
)


@router.get("/", response_model=List[LabelDisplay])
def get_all_labels(db: Annotated[Session, Depends(get_db)],
                   current_user: Annotated[UserBase, Depends(get_current_user)]):
    return crud_label.get_all_labels(db, user_id=current_user.id)


@router.post("/")
def create_label(db: Annotated[Session, Depends(get_db)],
                 current_user: Annotated[UserBase, Depends(get_current_user)],
                 request: LabelCreate):
    return crud_label.create(db, request, user_id=current_user.id)


@router.patch("/update/{label_id}", response_model=LabelDisplay)
def update_label(label_id: int,
                 db: Annotated[Session, Depends(get_db)],
                 current_user: Annotated[UserBase, Depends(get_current_user)],
                 request: LabelUpdate):
    return crud_label.update(db, request, user_id=current_user.id, label_id=label_id)
