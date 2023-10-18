from pydantic import BaseModel, ConfigDict
from fastapi import Form
from enum import Enum


class Status(str, Enum):
    to_do = "To Do"
    in_progress = "In Progress"
    review = "Review"


class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"


class TaskCreate(BaseModel):

    title: str
    description: str
    status: str = Status.to_do
    priority: str = Priority.low

    model_config = ConfigDict(
        extra="ignore",
        use_enum_values=True,
        validate_default=True
    )

    @classmethod
    def as_form(cls,
                title: str = Form(),
                description: str = Form(),
                status: Status = Form(),
                priority: Priority = Form(),
                ):
        return cls(title=title, description=description, status=status, priority=priority)


class TaskUpdate(BaseModel):
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None

    model_config = ConfigDict(
        use_enum_values=True,
        extra="ignore"
    )

    @classmethod
    def as_form(cls,
                title: str = Form(default=None),
                description: str = Form(default=None),
                status: Status = Form(default=None),
                priority: Priority = Form(default=None),
                ):
        return cls(title=title, description=description, status=status, priority=priority)
