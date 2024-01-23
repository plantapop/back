from datetime import datetime
from uuid import UUID, uuid4

from jose import jwt

from plantapop.shared.domain.entities import Entity
from plantapop.shared.domain.value_objects import GenericUUID


class Token(Entity):
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
        self._uuid = GenericUUID(uuid)
        self._token = token
        self._user_uuid = GenericUUID(user_uuid)
        self._token_type = token_type
        self._device = device
        self._exp = exp
        self._revoked = revoked

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
    ) -> "Token":
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

    @property
    def uuid(self) -> UUID:
        return self._uuid.get()

    @property
    def token(self) -> str:
        return self._token

    @property
    def user_uuid(self) -> UUID:
        return self._user_uuid.get()

    @property
    def token_type(self) -> str:
        return self._token_type

    @property
    def device(self) -> str:
        return self._device

    @property
    def exp(self) -> datetime:
        return self._exp

    @property
    def revoked(self) -> bool:
        return self._revoked

    def revoke(self) -> None:
        self._revoked = True
