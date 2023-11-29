from uuid import UUID

from plantapop.config import Config
from plantapop.shared.domain.token.exceptions import InvalidTokenException
from plantapop.shared.domain.token.token_validation_service import (
    TokenValidationService,
)

CONFIGMAP = Config().get_instance()


class ValidateToken:
    async def execute(self, token: str) -> UUID:
        validator = TokenValidationService(
            CONFIGMAP.jwt.key,
            CONFIGMAP.jwt.algorithm,
        )

        if not validator.is_valid(token, "access"):
            raise InvalidTokenException()

        return UUID(validator.payload["uuid"])
