from sqlalchemy.orm import Session
from app.models.user import DbUser
from app.schemas import UserCreate, UserUpdate
from app.database.hash import Hash
from typing import List


class CrudUser:
    def __init__(self):
        self.user_model = DbUser

    def get_by_id(self, db: Session, *, user_id: int) -> DbUser:
        return db.query(self.user_model).filter_by(id=user_id).first()

    def get_by_username(self, db: Session, *, username: str) -> DbUser:
        return db.query(self.user_model).filter_by(username=username).first()

    def get_by_email(self, db: Session, *, email: str) -> DbUser:
        return db.query(self.user_model).filter_by(email=email).first()

    def get_all(self, db: Session) -> List[DbUser]:
        return db.query(self.user_model).all()

    def create(self, db: Session, request: UserCreate) -> DbUser:
        new_user = self.user_model(
            name=request.name,
            surname=request.surname,
            username=request.username,
            email=request.email,
            password=Hash.bcrypt(request.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def update(self, db: Session, request: UserUpdate, *, user_id: int) -> DbUser:
        user = db.query(self.user_model).filter_by(id=user_id).first()
        if request.new_password and Hash.verify(request.old_password, user.password):
            setattr(user, "password", request.new_password)
        if request.email:
            setattr(user, "email", request.email)
        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, *, user_id: int) -> str:
        user = db.query(self.user_model).filter_by(id=user_id).first()
        setattr(user, "account", "deactivated")
        db.commit()
        return f"User {user.username} account has been deactivated"


crud_user = CrudUser()
