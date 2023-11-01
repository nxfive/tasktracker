from sqlalchemy.orm import Session
from app.models.user import DbUser
from app.schemas.user import UserCreate, UserUpdate
from app.database.hash import Hash
from app.crud.base import CrudBase


class CrudUser(CrudBase[DbUser]):
    def create(self, db: Session, request: UserCreate):
        new_user = self.model(
            **request.dict(exclude={"password", "confirm_password"}),
            password=Hash.bcrypt(request.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def update(self, db: Session, request: UserUpdate, *, user_id: int):
        user = db.query(self.model).filter_by(id=user_id).first()
        if request.new_password and Hash.verify(request.old_password, user.password):
            setattr(user, "password", request.new_password)
        if request.email:
            setattr(user, "email", request.email)
        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, *, user_id: int):
        user = db.query(self.model).filter_by(id=user_id).first()
        setattr(user, "account", "deactivated")
        db.commit()
        return f"User {user.username} account has been deactivated"


crud_user = CrudUser(DbUser)
