from datetime import datetime, timedelta
from typing import Union

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


# In the deployed app to be passed as environemntal variables :D
# This approach for testing only :)
SECRET_KEY = "5cd4b99178b3ba30e00c33496599954825b365a4ade55bd37ecceabaffbfdee1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": password_context.hash("admin")  # Only for testing:)
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]

        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict,
                        expires_delta: Union[timedelta, None] = None) -> str:

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
