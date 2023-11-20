from datetime import datetime, timedelta
from uuid import UUID

from plantapop.config import Config
from plantapop.shared.domain.token.token import Token

CONFIGMAP = Config().get_instance()


class TokenManager:
    def __init__(self):
        self.ac_duration = int(CONFIGMAP.jwt.access.duration)
        self.rf_duration = int(CONFIGMAP.jwt.refresh.duration)
        self.exp_margin = CONFIGMAP.jwt.refresh.refresh_expiration_margin

    def create_tokens(self, uuid: UUID, device: str) -> tuple[Token, Token]:
        access_token = self._create_token(uuid, device, token_type="access")
        refresh_token = self._create_token(uuid, device, token_type="refresh")
        return access_token, refresh_token

    def refresh_token(self, token: Token) -> tuple[Token, Token, bool]:
        access = self._create_token(
            token.get_user_uuid().get(), token.get_device(), token_type="access"
        )
        update = False

        if not self._is_token_expired(token, self.exp_margin):
            token = self._create_token(
                token.get_user_uuid().get(), token.get_device(), token_type="refresh"
            )
            update = True

        return access, token, update

    def _create_token(self, uuid: UUID, device: str, token_type: str) -> Token:
        duration = self.ac_duration if token_type == "access" else self.rf_duration
        return Token.create(
            user_uuid=uuid,
            token_type=token_type,
            device=device,
            exp=datetime.utcnow() + timedelta(seconds=duration),
            algorithm=CONFIGMAP.jwt.algorithm,
            key=CONFIGMAP.jwt.key,
        )

    @staticmethod
    def _is_token_expired(token: Token, expiration_margin: int) -> bool:
        return token.get_exp() <= datetime.utcnow() + timedelta(days=expiration_margin)
