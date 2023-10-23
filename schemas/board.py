from pydantic import BaseModel
from typing import List


class Label(BaseModel):
    name: str

    class Config:
        orm_mode = True


class BoardCreate(BaseModel):
    name: str


class BoardUpdate(BaseModel):
    name: str | None = None


class BoardDisplay(BaseModel):
    name: str
    labels: List[Label]

    class Config:
        orm_mode = True
