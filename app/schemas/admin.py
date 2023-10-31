from pydantic import BaseModel, EmailStr, root_validator
from fastapi import Form
from enum import Enum
from datetime import datetime
from app.schemas.tools import Validate


class Account(str, Enum):
    active = "active"
    deactivate = "deactivate"


class AdminCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    confirm_password: str

    @classmethod
    def as_form(
        cls,
        name: str = Form(),
        surname: str = Form(),
        email: EmailStr = Form(),
        password: str = Form(),
        confirm_password: str = Form(),
    ):
        return cls(
            name=name,
            surname=surname,
            email=email,
            password=password,
            confirm_password=confirm_password,
        )

    @classmethod
    @root_validator
    def verify_password_match(cls, values):
        password = values.get("password")
        confirm_password = values.get("confirm_password")

        if password != confirm_password:
            raise ValueError("Passwords did not match")
        return values


class AdminUpdate(BaseModel):
    email: EmailStr | None = None
    old_password: str | None = None
    new_password: str | None = None
    confirm_password: str | None = None

    @classmethod
    def as_form(
        cls,
        email: EmailStr = Form(),
        old_password: str = Form(),
        new_password: str = Form(),
        confirm_password: str = Form(),
    ):
        return cls(
            email=email,
            old_password=old_password,
            new_password=new_password,
            confirm_password=confirm_password,
        )

    @classmethod
    @root_validator(pre=True)
    def check_passwords(cls, values):
        Validate().validate_password_change(
            old=values.get("old_password", 0),
            new=values.get("new_password", 0),
            confirm=values.get("confirm_password", 0),
        )
        return values


class AdminDisplay(BaseModel):
    name: str
    surname: str
    email: EmailStr
    is_active: bool
    account: str
    created_at: datetime
    updated_at: datetime


class AdminUserDisplay(BaseModel):
    id: int
    name: str
    surname: str
    username: str
    email: EmailStr
    is_active: bool
    account: str
    created_at: datetime
    updated_at: datetime
