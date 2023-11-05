import logging
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from app.database.setup import get_db
from app.models.user import DbUser
from app.schemas.user import UserCreate, UserDisplay
from app.crud.user import crud_user
from app.database.hash import Hash
from app.auth import oauth2
from typing import Annotated
from datetime import timedelta

router = APIRouter(tags=["authentication"])


@router.post("/token")
def login(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = db.query(DbUser).filter_by(username=request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    access_token_expires = timedelta(
        minutes=oauth2.settings.access_token_expire_minutes
    )
    access_token = oauth2.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
    }


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserDisplay
)
def register(
    request: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    check_username = crud_user.get_by_attr(
        db, attr_name="username", value=request.username
    )
    if check_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken",
        )
    check_email = crud_user.get_by_attr(db, attr_name="email", value=request.email)
    if check_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email address is already associated with an account",
        )
    return crud_user.create(db, request)
