from database.setup import Base
from sqlalchemy import Column, Integer, String


class DbUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, index=True)
    password = Column(String)
