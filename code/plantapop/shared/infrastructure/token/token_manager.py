from datetime import datetime, timedelta
from uuid import UUID

from plantapop.config import Config
from plantapop.shared.domain.token.token import Token

CONFIGMAP = Config().get_instance()


class TokenManager:
    def __init__(self):
        self.access_token_duration = int(CONFIGMAP.jwt.access.duration)
        self.refresh_token_duration = int(CONFIGMAP.jwt.refresh.duration)

        self.key = CONFIGMAP.jwt.key
        self.algorithm = CONFIGMAP.jwt.algorithm
        self.expiration_margin = CONFIGMAP.jwt.refresh.refresh_expiration_margin

    def create_tokens(self, uuid: UUID, device: str) -> tuple[Token, Token]:
        access_token = self._create_access_token(uuid, device)
        refresh_token = self._create_refresh_token(uuid, device)

        return access_token, refresh_token

    def refresh_token(self, token: Token) -> tuple[Token, Token, bool]:
        access = self._create_access_token(
            token.get_user_uuid().get(), token.get_device()
        )
        update = False
        if not token.get_exp() <= datetime.utcnow() + timedelta(
            days=self.expiration_margin
        ):
            token = self._create_refresh_token(
                token.get_user_uuid().get(), token.get_device()
            )
            update = True
        return access, token, update

    def _create_access_token(self, uuid: UUID, device: str) -> Token:
        return Token.create(
            user_uuid=uuid,
            token_type="access",
            device=device,
            exp=datetime.utcnow() + timedelta(seconds=self.access_token_duration),
            algorithm=self.algorithm,
            key=self.key,
        )

    def _create_refresh_token(self, uuid: UUID, device: str) -> Token:
        return Token.create(
            user_uuid=uuid,
            token_type="refresh",
            device=device,
            exp=datetime.utcnow() + timedelta(seconds=self.refresh_token_duration),
            algorithm=self.algorithm,
            key=self.key,
        )
