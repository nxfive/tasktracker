from sqlalchemy import Column, Integer, String, Boolean, Enum
from database.setup import Base
from schemas.admin import Account


class DbAdmin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean)
    account = Column(Enum(Account), default=Account.active)
