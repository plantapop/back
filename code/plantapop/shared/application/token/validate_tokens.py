from uuid import UUID

from plantapop import CONFIGMAP
from plantapop.shared.domain.token.exceptions import InvalidTokenException
from plantapop.shared.domain.token.token_validation_service import (
    TokenValidationService,
)


class ValidateToken:
    def execute(self, token: str) -> UUID:
        validator = TokenValidationService(
            CONFIGMAP.jwt.key,
            CONFIGMAP.jwt.algorithm,
        )

        if not validator.is_valid(token, "access"):
            raise InvalidTokenException()

        return validator.token.get_user_uuid()
