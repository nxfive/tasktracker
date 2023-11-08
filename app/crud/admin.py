from sqlalchemy.orm import Session
from app.models.admin import DbAdmin
from app.schemas.admin import AdminCreate, AdminUpdate
from app.database.hash import Hash
from app.crud.base import CrudBase


class CrudAdmin(CrudBase[DbAdmin]):
    def create_admin(self, db: Session, request: AdminCreate) -> DbAdmin:
        new_admin = self.model(
            **request.dict(exclude={"password", "confirm_password"}),
            password=Hash.bcrypt(request.password),
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin

    def update_admin(
        self, db: Session, request: AdminUpdate, *, admin_id: int
    ) -> DbAdmin | None:
        admin = db.query(self.model).filter_by(id=admin_id).first()
        if request.new_password and Hash.verify(request.old_password, admin.password):
            setattr(admin, "password", request.new_password)
        if request.email:
            setattr(admin, "email", request.email)
        db.commit()
        db.refresh(admin)
        return admin


crud_admin = CrudAdmin(DbAdmin)
