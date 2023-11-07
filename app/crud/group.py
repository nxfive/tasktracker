from sqlalchemy.orm import Session
from app.models.group import DbGroup
from app.schemas.group import GroupCreate, GroupUpdate
from app.schemas.user import UserGet
from app.models.user import DbUser
from typing import Optional, List, Dict
from app.crud.base import CrudBase
from fastapi import HTTPException, status


class CrudGroup(CrudBase[DbGroup]):
    def get_all_groups(self, db: Session, *, user_id: int) -> list[DbGroup]:
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
        new_group = self.model(**request.dict(), owner_id=user_id)
        for admin in request.admins:
            user = db.query(DbUser).filter_by(username=admin.username).first()
            if user:
                new_group.admins.append(user)

        for member in request.members:
            user = db.query(DbUser).filter_by(username=member.username).first()
            if user:
                new_group.members.append(user)
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
        return new_group

    def update(self, db: Session, request: GroupUpdate, group: DbGroup):
        """
        This method can only update information about group:
         - name
         - description
         - visibility
        """

        # TO DO: nie moze w takim razie przyjmowac wszystkich argumentow

        data = request.dict(exclude_unset=True, exclude={"admins", "members"})

        for key, value in data.items():
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
    ) -> Dict[str, str]:
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


crud_group = CrudGroup(DbGroup)
