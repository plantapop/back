from datetime import datetime, timedelta

import jose

from plantapop import CONFIGMAP
from plantapop.shared.domain.value_objects import GenericUUID


class TokenManager:
    def __init__(self):
        self.access_token_duration = CONFIGMAP.jwt.access.duration
        self.refresh_token_duration = CONFIGMAP.jwt.refresh.duration

        self.key = CONFIGMAP.jwt.key
        self.algorithm = CONFIGMAP.jwt.algorithm

    def create_tokens(self, uuid: GenericUUID) -> dict[str, str]:
        access_token = self.create_access_token(uuid)
        refresh_token = self.create_refresh_token(uuid)

        return {"access": access_token, "refresh": refresh_token}

    def validate_token(self, token: str) -> dict:
        try:
            return jose.jwt.decode(
                token,
                self.key,
                algorithms=[self.algorithm],
                options={"verify_aud": False},
            )
        except jose.JWTError:
            return {}

    def create_access_token(self, uuid: GenericUUID) -> str:
        return jose.jwt.encode(
            {
                "exp": datetime.utcnow()
                + timedelta(seconds=self.access_token_duration),
                "uuid": uuid.get(),
                "type": "access",
            },
            self.key,
            algorithm=self.algorithm,
        )

    def create_refresh_token(self, uuid: GenericUUID) -> str:
        return jose.jwt.encode(
            {
                "exp": datetime.utcnow()
                + timedelta(seconds=self.refresh_token_duration),
                "uuid": uuid.get(),
                "type": "refresh",
            },
            self.key,
            algorithm=self.algorithm,
        )
