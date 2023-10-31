from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from app.database import Base
from sqlalchemy.ext.declarative import ConcreteBase


class Board(ConcreteBase, Base):
    __tablename__ = "boards"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String)
    labels = relationship("DbLabel", back_populates="board")

    __mapper_args__ = {
        "polymorphic_identity": "boards",
        "concrete": True,
    }


class DbUserBoard(Board):
    __tablename__ = "userBoards"
    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("DbUser", back_populates="boards")
    labels = relationship("DbLabel", back_populates="board")

    __mapper_args__ = {
        "polymorphic_identity": "userBoards",
        "concrete": True,
    }


class DbRemoteBoard(Board):
    __tablename__ = "remoteBoards"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String)
    group_id = mapped_column(Integer, ForeignKey("groups.id"))
    group = relationship("DbGroup", back_populates="board")
    labels = relationship("DbLabel", back_populates="board")

    __mapper_args__ = {
        "polymorphic_identity": "remoteBoards",
        "concrete": True,
    }
