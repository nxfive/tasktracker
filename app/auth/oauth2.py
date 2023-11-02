from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.database.setup import get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud.user import crud_user
from app.schemas.user import UserCheck
from typing import Annotated
from app.core.config import get_settings
from app.exceptions.custom import EntityNotExist

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, str(settings.secret_key), algorithm=settings.algorithm
    )
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # verify token
        payload = jwt.decode(
            token, str(settings.secret_key), algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud_user.get_by_attr(db, attr_name="username", value=username)
    if user is None:
        raise credentials_exception
    return user


def get_superuser(user: UserCheck = Depends(get_current_user)):
    if user.role != "admin":
        raise EntityNotExist("user")
    return user
