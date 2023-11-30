from plantapop.config import Config
from plantapop.shared.domain.token.exceptions import InvalidTokenException
from plantapop.shared.domain.token.token_validation_service import (
    TokenValidationService,
)
from plantapop.shared.infrastructure.token.token_manager import TokenManager
from plantapop.shared.infrastructure.token.token_repository import RefreshTokenUoW

CONFIGMAP = Config().get_instance()


class RefreshToken:
    def __init__(self):
        self.uow = RefreshTokenUoW()
        self.token_factory = TokenManager()

    async def execute(self, token: str) -> dict[str, str]:
        async with self.uow as repo:
            val = TokenValidationService(
                key=CONFIGMAP.jwt.key,
                algorithm=CONFIGMAP.jwt.algorithm,
                repository=repo,
            )

            if not val.is_valid(token, "refresh") or await val.is_revoked(token):
                raise InvalidTokenException()

            access, refresh, refresh_updated = self.token_factory.refresh_token(
                val.token
            )

            if refresh_updated:
                val.token.revoke()
                await repo.save(val.token)
                await repo.save(refresh)

        return {"access": access.token, "refresh": refresh.token}
