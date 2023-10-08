from datetime import datetime
from typing import Union

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from plantapop import CONFIGMAP


class JWTValidator:
    @staticmethod
    def validate(token: str) -> dict[str, Union[str, datetime]]:
        try:
            payload = jwt.decode(
                token,
                CONFIGMAP.JWT.SECRET,
                algorithms=[CONFIGMAP.JWT.ALGORITHM],
            )
            assert payload["scope"] == CONFIGMAP.JWT.ACCESS_SCOPE, "Invalid scope"
            return payload

        except ExpiredSignatureError:
            raise Exception("Token expired")  # TODO: Create custom exception
        except JWTError:
            raise Exception("Invalid token")
