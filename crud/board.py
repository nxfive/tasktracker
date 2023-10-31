from models.board import DbUserBoard, DbRemoteBoard
from schemas.board import BoardCreate, BoardUpdate
from sqlalchemy.orm import Session
from models.user import DbUser


class CrudUserBoard:

    def __init__(self):
        self.model = DbUserBoard

    def get_all_boards(self, db: Session, *, user_id):
        return db.query(self.model).filter_by(user_id=user_id).all()

    def create(self, db: Session, request: BoardCreate, user_id: int):
        new_board = self.model(
            name=request.name,
            user_id=user_id
        )
        db.add(new_board)
        db.commit()
        db.refresh(new_board)
        return new_board

    def update(self, db: Session, request: BoardUpdate, user_id: int, board_id: int):
        board = db.query(self.model).filter_by(id=board_id).first()
        if user_id == board.user_id:
            data = request.dict(exclude_unset=True)
            for key, value in data.items():
                setattr(board, key, value)
            db.commit()
            db.refresh(board)
            return board


crud_board = CrudUserBoard()
