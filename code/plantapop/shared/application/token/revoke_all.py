from uuid import UUID

from plantapop.shared.domain.specification.filter import Equals
from plantapop.shared.domain.specification.specification import Specification
from plantapop.shared.domain.token.token import Token
from plantapop.shared.infrastructure.token.token_repository import RefreshTokenUoW


class RevokeAll:
    def __init__(self):
        self.uow = RefreshTokenUoW()

    def execute(self, user_uuid: UUID) -> None:
        with self.uow as repo:
            tokens: list[Token] = repo.matching(
                Specification(
                    filter=Equals("user_uuid", user_uuid) & Equals("revoked", False)
                )
            )
            for token in tokens:
                token.revoke()

            repo.save_all(tokens)
