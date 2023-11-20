from uuid import UUID

from plantapop.shared.domain.specification import filter, specification
from plantapop.shared.infrastructure.token.token_manager import TokenManager
from plantapop.shared.infrastructure.token.token_repository import RefreshTokenUoW


class CreateToken:
    def __init__(self):
        self.uow = RefreshTokenUoW
        self.token_factory = TokenManager()

    def execute(self, uuid: UUID, device: str) -> dict[str, str]:
        with self.uow() as repo:
            existing_token = repo.matching(
                specification.Specification(
                    filter.Equals("user_uuid", uuid) & filter.Equals("device", device)
                )
            )

            if existing_token:
                existing_token.revoke()
                self.token_repository.save(existing_token)

            access, refresh = self.token_factory.create_tokens(uuid, device)

            repo.save(refresh)

        return {"access": access.token, "refresh": refresh.token}
