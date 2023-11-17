from uuid import UUID

from plantapop.shared.domain.token.token import Token
from plantapop.shared.infrastructure.token.token_repository import (
    RefreshJwtTokenRepository,
)


class RevokeAll:
    def __init__(self):
        self.token_repository = RefreshJwtTokenRepository()

    def execute(self, user_uuid: UUID) -> None:
        tokens: list[Token] = self.token_repository.find_all_by_user(user_uuid)
        for token in tokens:
            token.revoke()

        self.token_repository.save_all(tokens)
