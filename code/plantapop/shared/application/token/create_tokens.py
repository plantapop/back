from uuid import UUID

from plantapop.shared.domain.specification import filter, specification
from plantapop.shared.domain.value_objects import GenericUUID
from plantapop.shared.infrastructure.token.token_manager import TokenManager
from plantapop.shared.infrastructure.token.token_repository import RefreshTokenUoW


class CreateToken:
    def __init__(self):
        self.uow = RefreshTokenUoW()
        self.token_factory = TokenManager()

    def execute(self, uuid: UUID, device: str) -> dict[str, str]:
        with self.uow as repo:
            self._check_token(repo, uuid, device)

            access, refresh = self.token_factory.create_tokens(uuid, device)

            repo.save(refresh)

        return {"access": access.token, "refresh": refresh.token}

    def _check_token(self, repo, uuid, device):
        existing_token = repo.matching(
            specification.Specification(
                filter.Equals("user_uuid", GenericUUID(uuid))
                & filter.Equals("device", device)
                & filter.Equals("revoked", False)
            )
        )

        if existing_token:
            token = existing_token[0]
            token.revoke()
            repo.update(token)
