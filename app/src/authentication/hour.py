from datetime import datetime

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

import src.authentication.authentication as ath


async def get_current_time(token: str = Depends(ath.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, ath.SECRET_KEY, algorithms=[ath.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return datetime.now().strftime("%H:%M:%S")
