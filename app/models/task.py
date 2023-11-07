from app.database.setup import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.schemas.task import Priority, Status


class DbTask(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    status = Column(Enum(Status), default=Status.to_do)
    priority = Column(Enum(Priority), default=Priority.low)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("DbUser", back_populates="tasks")
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.now())
