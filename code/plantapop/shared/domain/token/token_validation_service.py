from jose import jwt
from jose.exceptions import JWTError

from plantapop.shared.domain.repositories import GenericRepository
from plantapop.shared.domain.specification.filter import Equals
from plantapop.shared.domain.specification.specification import Specification
from plantapop.shared.domain.token.token import Token


class TokenValidationService:
    def __init__(
        self, key: str, algorithm: str, repository: GenericRepository | None = None
    ):
        self.repository = repository
        self.key = key
        self.algorithm = algorithm

    def is_valid(self, token: str, token_type: str) -> bool:
        try:
            self._payload = jwt.decode(
                token,
                self.key,
                algorithms=[self.algorithm],
                options={"verify_aud": False},
            )
            return self._payload["type"] == token_type
        except JWTError:
            return False

    async def is_revoked(self, token: str) -> bool:
        if not self.repository:
            raise Exception("Repository not set")

        self._token: Token = (
            await self.repository.matching(Specification(filter=Equals("token", token)))
        )[0]

        return self._token.revoked

    @property
    def payload(self) -> dict:
        if not self._payload:
            raise Exception("Payload not set")
        return self._payload

    @property
    def token(self) -> Token:
        if not self._token:
            raise Exception("Token not set")
        return self._token
