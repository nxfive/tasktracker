from database.setup import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models.group import group_admins, group_members


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
    tasks = relationship("DbTask", back_populates="user")
    owned_groups = relationship("DbGroup", back_populates="owner")
    admin_of_groups = relationship("DbGroup", secondary=group_admins, back_populates="admins")
    member_of_groups = relationship("DbGroup", secondary=group_members, back_populates="members")
