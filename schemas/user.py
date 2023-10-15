from pydantic import BaseModel, EmailStr
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


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    old_password: str | None = None
    new_password: str | None = None

