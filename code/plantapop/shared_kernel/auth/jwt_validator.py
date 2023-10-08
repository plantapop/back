from datetime import datetime
from typing import Union

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from plantapop import CONFIGMAP


class JWTValidator:
    @staticmethod
    def validate(token: str) -> dict[str, Union[str, datetime]]:
        try:
            return jwt.decode(
                token,
                CONFIGMAP.get("JWT_SECRET"),
                algorithms=[CONFIGMAP.get("JWT_ALGORITHM")],
            )
        except ExpiredSignatureError:
            raise Exception("Token expired")  # TODO: Create custom exception
        except JWTError:
            raise Exception("Invalid token")
