from sqlalchemy.orm import Session
from app.models.group import DbGroup
from app.schemas.group import GroupCreate, GroupUpdate
from app.models.user import DbUser
from typing import Optional, List, Dict


class CrudGroup:
    def __init__(self):
        self.model = DbGroup

    def get_by_id(self, db: Session, *, group_id: int) -> DbGroup:
        return db.query(self.model).filter(self.model.id == group_id).first()

    def get_all_groups(self, db: Session, *, user_id: int) -> List[DbGroup]:
        groups = (
            db.query(self.model)
            .filter(
                (self.model.owner_id == user_id)
                | (self.model.admins.any(id=user_id))
                | (self.model.members.any(id=user_id))
            )
            .all()
        )
        return groups

    def create(self, db: Session, request: GroupCreate, *, user_id: int) -> DbGroup:
        new_group = self.model(
            name=request.name,
            description=request.description,
            owner_id=user_id,
            visibility=request.visibility,
        )
        admin_users = []
        for admin in request.admins:
            user = db.query(DbUser).filter_by(username=admin.username).first()
            if user:
                admin_users.append(user)

        member_users = []
        for member in request.members:
            user = db.query(DbUser).filter_by(username=member.username).first()
            if user:
                member_users.append(user)
        new_group.admins = admin_users
        new_group.members = member_users
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
        return new_group

    def update(
        self,
        db: Session,
        request: GroupUpdate,
        group: Optional[DbGroup] = None,
        *,
        group_id: Optional[int] = None,
        user_id: Optional[int] = None
    ):
        group = db.query(self.model).filter_by(id=group_id).first()
        is_admin = [admin for admin in group.admins if admin.id == user_id]
        if group.owner_id == user_id or is_admin:
            request_data = request.dict(exclude_unset=True)
            for key, value in request_data.items():
                if key == "admins":
                    admins_usernames = [value[i]["username"] for i in range(len(value))]
                    for username in admins_usernames:
                        admin = db.query(DbUser).filter_by(username=username).first()
                        if admin:
                            group.admins.append(admin)
                elif key == "members":
                    members_usernames = [
                        value[i]["username"] for i in range(len(value))
                    ]
                    for username in members_usernames:
                        member = db.query(DbUser).filter_by(username=username).first()
                        if member:
                            group.members.append(member)
                else:
                    if value is not None:
                        setattr(group, key, value)
            db.commit()
            db.refresh(group)
        return group

    def delete(
        self,
        db: Session,
        group: Optional[DbGroup] = None,
        *,
        group_id: Optional[int] = None,
        user_id: Optional[int] = None
    ) -> Dict[str]:
        # only owner can delete his own group
        if not (group or group_id and user_id):
            return {"error": "Not enough data to process"}
        elif group:
            db.delete(group)
            db.commit()
        else:
            group = db.query(self.model).filter_by(id=group_id).first()
            if group.owner_id == user_id:
                db.delete(group)
                db.commit()
        return {"message": "group deleted"}


crud_group = CrudGroup()
