from uuid import UUID
from plantapop.shared.infrastructure.token.token_repository import TokenRepository
from plantapop.shared.domain.token.token import Token


class RevokeAll:
    def __init__(self):
        self.token_repository = TokenRepository()

    def execute(self, user_uuid: UUID) -> None:
        tokens: list[Token] = self.token_repository.find_by_user_uuid(user_uuid)
        for token in tokens:
            token.revoke()

        self.token_repository.save_all(tokens)

