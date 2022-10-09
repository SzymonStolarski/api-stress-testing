from datetime import datetime
import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)


async def get_current_time(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    secret_key = os.environ['SECRET_KEY']
    algorithm = os.environ['ALGORITHM']

    try:
        payload = jwt.decode(key=secret_key, algorithms=algorithm, token=token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return datetime.now().strftime("%H:%M:%S")


@router.get("/time/get")
def current_time(time: datetime = Depends(get_current_time)):
    return time
