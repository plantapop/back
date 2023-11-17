from plantapop import CONFIGMAP
from plantapop.shared.domain.token.exceptions import InvalidTokenException
from plantapop.shared.domain.token.token_validation_service import (
    TokenValidationService,
)
from plantapop.shared.infrastructure.token.token_manager import TokenManager
from plantapop.shared.infrastructure.token.token_repository import TokenRepository


class RefreshToken:
    def __init__(self):
        self.token_repository = TokenRepository()
        self.token_factory = TokenManager()

    def execute(self, token: str) -> dict[str, str]:
        validator = TokenValidationService(
            CONFIGMAP.jwt.key, CONFIGMAP.jwt.algorithm, self.token_repository
        )

        if not validator.is_valid(token, "refresh") or validator.is_revoked(token):
            raise InvalidTokenException()

        access, refresh, refresh_updated = self.token_factory.refresh_token(
            validator.token
        )

        if refresh_updated:
            validator.token.revoke()
            self.token_repository.save(validator.token)
            self.token_repository.save(refresh)

        return {"access": access.token, "refresh": refresh.token}
