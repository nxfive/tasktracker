from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from app.database import Base
from app.schemas.admin import Account
from datetime import datetime


class DbAdmin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean)
    account = Column(Enum(Account), default=Account.active)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.now())
