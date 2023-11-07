from app.database.setup import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

group_admins = Table(
    "group_admins",
    Base.metadata,
    Column("admin_id", ForeignKey("users.id")),
    Column("group_id", ForeignKey("groups.id")),
)

group_members = Table(
    "group_members",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("group_id", ForeignKey("groups.id")),
)


class DbGroup(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("DbUser", back_populates="owned_groups")
    admins = relationship(
        "DbUser", secondary="group_admins", back_populates="admin_of_groups"
    )
    members = relationship(
        "DbUser", secondary="group_members", back_populates="member_of_groups"
    )
    visibility = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())
    board = relationship("DbRemoteBoard", back_populates="group")
