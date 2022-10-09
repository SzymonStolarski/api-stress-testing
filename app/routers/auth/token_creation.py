from datetime import datetime, timedelta
import os
from typing import Union

from jose import jwt


class TokenCreator:

    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: Union[timedelta, None] = None
                            ) -> str:

        to_encode = data.copy()
        key = os.environ['SECRET_KEY']
        algorithm = os.environ['ALGORITHM']

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            key=key,
            algorithm=algorithm)

        return encoded_jwt
