from pydantic import BaseModel
from typing import List
from datetime import datetime


class User(BaseModel):
    username: str


class GroupCreate(BaseModel):
    name: str
    description: str
    visibility: bool
    admins: List[User] | None = None
    members: List[User] | None = None


class GroupUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    visibility: bool | None = None
    admins: List[User] | None = None
    members: List[User] | None = None


class GroupDisplay(BaseModel):
    name: str
    description: str
    visibility: bool
    owner: User
    admins: List[User]
    members: List[User]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
