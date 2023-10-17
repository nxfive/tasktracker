from pydantic import BaseModel, EmailStr, root_validator
from fastapi import Form


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
        password = values.get("password")
        confirm_password = values.get("confirm_password")

        if password != confirm_password:
            raise ValueError("Passwords did not match")
        return values


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    old_password: str | None = None
    new_password: str | None = None

    @classmethod
    def as_form(cls,
                email: str = Form(),
                old_password: str = Form(),
                new_password: str = Form()):
        return cls(
            email=email,
            old_password=old_password,
            new_password=new_password
        )

    @classmethod
    @root_validator(pre=True)
    def check_passwords(cls, values):
        if "new_password" in values and "old_password" not in values:
            raise ValueError("Old password must be provided!")
        return values


class UserDisplay(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr

    class Config:
        orm_mode: True
