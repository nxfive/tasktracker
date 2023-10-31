from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from database.setup import Base
from sqlalchemy.orm import relationship, mapped_column


class DbLabel(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    color = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("DbUser", back_populates="labels")
    board_id = mapped_column(Integer, ForeignKey("boards.id"))
    board = relationship("Board", back_populates="labels")

