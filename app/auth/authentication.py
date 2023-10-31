from fastapi import APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from app.database.setup import get_db
from app.models.user import DbUser
from app.database.hash import Hash
from app.auth import oauth2
from typing import Annotated
from datetime import timedelta


router = APIRouter(tags=["authentication"])


@router.post("/token")
async def login(
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
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )
    access_token_expires = timedelta(minutes=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = oauth2.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
    }
