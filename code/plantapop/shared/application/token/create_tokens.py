from uuid import UUID

from plantapop.shared.infrastructure.token.token_manager import TokenManager
from plantapop.shared.infrastructure.token.token_repository import (
    RefreshJwtTokenRepository,
)


class CreateToken:
    def __init__(self):
        self.token_repository = RefreshJwtTokenRepository()
        self.token_factory = TokenManager()

    def execute(self, uuid: UUID, device: str) -> dict[str, str]:
        existing_token = self.token_repository.get_token_by_user_and_device(
            uuid, device
        )

        if existing_token:
            existing_token.revoke()
            self.token_repository.save(existing_token)

        access, refresh = self.token_factory.create_tokens(uuid, device)

        self.token_repository.save(refresh)

        return {"access": access.token, "refresh": refresh.token}
