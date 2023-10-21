from pydantic import BaseModel
from typing import List


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
