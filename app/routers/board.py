from fastapi import APIRouter, Depends
from typing import List, Annotated
from app.schemas.board import BoardUpdate, BoardCreate, BoardDisplay
from app.schemas.user import UserBase
from app.database import get_db
from app.auth import get_current_user
from sqlalchemy.orm import Session
from app.crud.board import crud_board


router = APIRouter(
    prefix="/boards",
    tags=["boards"]
)


@router.get("/", response_model=List[BoardDisplay])
def get_all_boards(db: Annotated[Session, Depends(get_db)],
                   current_user: Annotated[UserBase, Depends(get_current_user)]):
    return crud_board.get_all_boards(db, user_id=current_user.id)


@router.post("/")
def create_board(db: Annotated[Session, Depends(get_db)],
                 current_user: Annotated[UserBase, Depends(get_current_user)],
                 request: BoardCreate):
    return crud_board.create(db, request, user_id=current_user.id)


@router.patch("/update/{board_id}", response_model=BoardDisplay)
def update_board(board_id: int,
                 db: Annotated[Session, Depends(get_db)],
                 current_user: Annotated[UserBase, Depends(get_current_user)],
                 request: BoardUpdate):
    return crud_board.update(db, request, user_id=current_user.id, board_id=board_id)



