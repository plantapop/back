from datetime import datetime as dt
from datetime import timedelta as td
from uuid import UUID, uuid4

from plantapop.config import Config
from plantapop.shared.domain.token.token import Token

CONFIGMAP = Config.get_instance()


class RefreshTokenMother:
    @staticmethod
    def create(
        user_uuid: UUID = uuid4(),
        token_type: str = "refresh",
        device: str = "device",
        exp: dt = dt.now() + td(days=1),
        revoked: bool = False,
        algorithm: str = CONFIGMAP.jwt.algorithm,
        key: str = CONFIGMAP.jwt.key,
    ) -> Token:
        return Token.create(
            user_uuid=user_uuid,
            token_type=token_type,
            device=device,
            exp=exp,
            algorithm=algorithm,
            key=key,
            revoked=revoked,
        )
