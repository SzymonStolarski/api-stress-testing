from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from db.fake_users_db import fake_users_db
from entities.token import Token
from routers.auth.user_authentication import UserAuthenticator
from routers.auth.token_creation import *


router = APIRouter()


@router.post("/auth/token", response_model=Token)
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserAuthenticator.authenticate_user(
        fake_users_db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    expiration = int(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'])
    access_token_expires = timedelta(minutes=expiration)
    access_token = TokenCreator.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
