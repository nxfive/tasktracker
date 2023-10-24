from models.admin import DbAdmin
from schemas.admin import AdminCreate, AdminUpdate
from sqlalchemy.orm import Session
from database.hash import Hash
from crud.user import CrudUser


class CrudAdmin(CrudUser):

    def __init__(self):
        super().__init__()
        self.admin_model = DbAdmin

    def get_all_admins(self, db: Session):
        return db.query(self.admin_model).all()

    def create_admin(self, db: Session, request: AdminCreate):
        new_admin = self.admin_model(
            name=request.name,
            surname=request.surname,
            email=request.email,
            password=Hash.bcrypt(request.password)
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin

    def update(self, db: Session, request: AdminUpdate, *, admin_id: int):
        admin = db.query(self.admin_model).filter_by(id=admin_id).first()
        if request.new_password and Hash.verify(request.old_password, admin.password):
            setattr(admin, "password", request.new_password)
        if request.email:
            setattr(admin, "email", request.email)
        db.commit()
        db.refresh(admin)
        return admin

    def assign(self, db: Session, user_id: int):
        user = db.query(self.user_model).filter_by(id=user_id).first()
        setattr(user, "role", "admin")
        return {
            "message": f"User {user.username} role has changed to admin"
        }


crud_admin = CrudAdmin()
