from jose import jwt
from jose.exceptions import JWTError

from plantapop.shared.domain.token.token import Token
from plantapop.shared.domain.token.token_repository import TokenRepository


class TokenValidationService:
    def __init__(
        self, key: str, algorithm: str, repository: TokenRepository | None = None
    ):
        self.repository = repository
        self.key = key
        self.algorithm = algorithm
        self.token: Token | None = None
        self.payload: dict | None = None

    def is_valid(self, token: str, token_type: str) -> bool:
        try:
            decoded = jwt.decode(
                token,
                self.key,
                algorithms=[self.algorithm],
                options={"verify_aud": False},
            )
            self.payload = decoded
            return decoded["type"] == token_type
        except JWTError:
            return False

    def is_revoked(self, token: str) -> bool:
        if not self.repository:
            raise Exception("Token repository not set")

        self.token: Token = self.repository.get(token)  # Should Always return a token

        return self.token.is_revoked()
