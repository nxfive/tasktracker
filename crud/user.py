from sqlalchemy.orm import Session
from models.user import DbUser
from schemas.user import UserCreate, UserUpdate
from database.hash import Hash


class CrudUser:

    def __init__(self):
        self.model = DbUser

    def get_user_by_username(self, db: Session, *, username: str):
        return db.query(self.model).filter_by(username=username).first()

    def get_all_users(self, db: Session):
        return db.query(self.model).all()

    def create_user(self, db: Session, request: UserCreate):
        new_user = self.model(
            name=request.name,
            surname=request.surname,
            username=request.username,
            email=request.email,
            password=Hash.bcrypt(request.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def update_user(self, db: Session, request: UserUpdate, *, user_id: int):
        user = db.query(self.model).filter_by(id=user_id).first()
        if request.new_password and Hash.verify(request.old_password, user.password):
            setattr(user, "password", request.new_password)
        if request.email:
            setattr(user, "email", request.email)
        db.commit()
        db.refresh(user)
        return user

    def delete_user(self, db: Session, *, user_id: int):
        user = db.query(self.model).filter_by(id=user_id).first()
        setattr(user, "account", "deactivated")
        db.commit()
        return f"User {user.username} account has been deactivated"


crud_user = CrudUser()
