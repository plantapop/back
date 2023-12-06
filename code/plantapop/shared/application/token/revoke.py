from uuid import UUID

from plantapop.shared.domain.specification.filter import Equals
from plantapop.shared.domain.specification.specification import Specification
from plantapop.shared.domain.token.token import Token
from plantapop.shared.infrastructure.token.token_repository import RefreshTokenUoW


class Revoke:
    def __init__(self):
        self.uow = RefreshTokenUoW()

    async def execute(
        self, user_uuid: UUID, device: str | None = None, rall: bool | None = None
    ) -> None:
        filter = Equals("user_uuid", user_uuid) & Equals("revoked", False)

        if not rall and not device:
            raise Exception("Must provide device or all")
        if device:
            filter &= Equals("device", device)

        async with self.uow as repo:
            tokens: list[Token] = await repo.matching(
                Specification(
                    filter=filter,
                )
            )
            for token in tokens:
                token.revoke()

            await repo.save_all(tokens)
