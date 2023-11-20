from datetime import datetime
from uuid import UUID, uuid4

from jose import jwt

from plantapop.shared.domain.value_objects import GenericUUID


class Token:
    def __init__(
        self,
        uuid: UUID,
        token: str,
        user_uuid: UUID,
        token_type: str,
        device: str,
        exp: datetime,
        revoked: bool,
    ):
        self.uuid = GenericUUID(uuid)
        self.token = token
        self.user_uuid = GenericUUID(user_uuid)
        self.token_type = token_type
        self.device = device
        self.exp = exp
        self.revoked = revoked

    @classmethod
    def create(
        cls,
        user_uuid: UUID,
        token_type: str,
        device: str,
        exp: datetime,
        algorithm: str,
        key: str,
        revoked: bool = False,
    ) -> str:
        token = jwt.encode(
            {
                "exp": exp,
                "uuid": str(user_uuid),
                "type": token_type,
                "device": device,
            },
            key,
            algorithm=algorithm,
        )

        return cls(uuid4(), token, user_uuid, token_type, device, exp, revoked)

    def revoke(self) -> None:
        self.revoked = True

    def is_revoked(self) -> bool:
        return self.revoked

    def get(self) -> str:
        return self.token

    def get_user_uuid(self) -> str:
        return self.user_uuid

    def get_device(self) -> str:
        return self.device

    def get_exp(self) -> datetime:
        return self.exp
