from app.database.setup import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from app.models.group import group_admins, group_members
from app.schemas import Role
from datetime import datetime


class DbUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    account = Column(String, default="active")
    role = Column(Enum(Role), default="user")
    tasks = relationship("DbTask", back_populates="user")
    owned_groups = relationship("DbGroup", back_populates="owner")
    admin_of_groups = relationship(
        "DbGroup", secondary=group_admins, back_populates="admins"
    )
    member_of_groups = relationship(
        "DbGroup", secondary=group_members, back_populates="members"
    )
    # labels = relationship("DbLabel", back_populates="creator")
    # boards = relationship("DbUserBoard", back_populates="user")
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.now())
