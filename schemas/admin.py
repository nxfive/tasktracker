from pydantic import BaseModel, EmailStr, root_validator
from fastapi import Form
from enum import Enum


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
    def as_form(cls,
                name: str = Form(),
                surname: str = Form(),
                email: EmailStr = Form(),
                password: str = Form(),
                confirm_password: str = Form()
                ):
        return cls(name=name, surname=surname, email=email, password=password, confirm_password=confirm_password)

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
    password: str | None = None
    confirm_password: str | None = None

    @classmethod
    def as_form(cls,
                email: EmailStr = Form(),
                password: str = Form(),
                confirm_password: str = Form()
                ):
        return cls(email=email, password=password, confirm_password=confirm_password)

    @classmethod
    @root_validator(pre=True)
    def check_passwords(cls, values):
        if "new_password" in values and "old_password" not in values:
            raise ValueError("Old password must be provided!")
        return values
