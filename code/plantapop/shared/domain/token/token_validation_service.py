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
        self.token: Token | None = None
        self.payload: dict | None = None

    def is_valid(self, token: str, token_type: str) -> bool:
        try:
            self.payload = jwt.decode(
                token,
                self.key,
                algorithms=[self.algorithm],
                options={"verify_aud": False},
            )
            return self.payload["type"] == token_type
        except JWTError:
            return False

    async def is_revoked(self, token: str) -> bool:
        self.token: Token = (
            await self.repository.matching(Specification(filter=Equals("token", token)))
        )[0]

        return self.token.is_revoked()
