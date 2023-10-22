from models.group import DbGroup
from models.user import DbUser
from schemas.group import GroupCreate, GroupUpdate
from sqlalchemy.orm import Session


class CrudGroup:

    def __init__(self):
        self.model = DbGroup

    def get_all_groups(self, db: Session, *, user_id):
        groups = db.query(self.model).filter(
                        (self.model.owner_id == user_id)
                        | (self.model.admins.any(id=user_id))
                        | (self.model.members.any(id=user_id))
        ).all()
        return groups

    def create(self, db: Session, request: GroupCreate, *, user_id):
        new_group = self.model(
            name=request.name,
            description=request.description,
            owner_id=user_id,
            admins=request.admins,
            members=request.members,
            visibility=request.visibility
        )
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
        return new_group

    def update(self, db: Session, request: GroupUpdate, *, group_id, user_id):
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
                    members_usernames = [value[i]["username"] for i in range(len(value))]
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

    def delete(self, db: Session, *, group_id: int, user_id: int):
        # only owner can delete his own group
        group = db.query(self.model).filter_by(id=group_id).first()
        if group.owner_id == user_id:
            db.delete(group)
            db.commit()
        return {"message": "group deleted"}


crud_group = CrudGroup()
