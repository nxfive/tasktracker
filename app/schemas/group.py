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


class GroupUpdateAdmins(BaseModel):
    admins: List[User] | None = None


class GroupUpdateMembers(BaseModel):
    members: List[User] | None = None


class UserDisplay(BaseModel):
    username: str

    class Config:
        orm_mode = True


class GroupDisplay(BaseModel):
    name: str
    description: str
    visibility: bool
    owner: UserDisplay
    admins: List[UserDisplay] | None = None
    members: List[UserDisplay] | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
