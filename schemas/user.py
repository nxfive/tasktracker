from pydantic import BaseModel, EmailStr, root_validator
from fastapi import Form
from enum import Enum
from schemas.tools import Validate


class Role(str, Enum):
    admin = "admin"
    user = "user"


class UserBase(BaseModel):
    id: int


class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr
    password: str
    confirm_password: str

    @classmethod
    def as_form(cls, name: str = Form(),
                surname: str = Form(),
                username: str = Form(),
                email: str = Form(),
                password: str = Form(),
                confirm_password: str = Form()):
        return cls(
            name=name,
            surname=surname,
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password
        )

    @classmethod
    @root_validator
    def verify_password_match(cls, values):
        Validate().validate_passwords_match(new=values.get("password", 0), confirm=values.get("confirm_password", 0))
        return values


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    old_password: str | None = None
    new_password: str | None = None
    confirm_password: str | None = None

    @classmethod
    def as_form(cls,
                email: str = Form(),
                old_password: str = Form(),
                new_password: str = Form(),
                confirm_password: str = Form()):
        return cls(
            email=email,
            old_password=old_password,
            new_password=new_password,
            confirm_password=confirm_password
        )

    @classmethod
    @root_validator(pre=True)
    def check_passwords(cls, values):
        Validate.validate_password_change(
            old=values.get("old_password", 0),
            new=values.get("new_password", 0),
            confirm=values.get("confirm_password", 0)
        )
        return values


class UserDisplay(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr

    class Config:
        orm_mode: True
