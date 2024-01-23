from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String, Uuid

from plantapop.shared.domain.token.token import Token
from plantapop.shared.infrastructure.repository.data_mapper import DataMapper
from plantapop.shared.infrastructure.repository.database import Base
from plantapop.shared.infrastructure.repository.specification_mapper import (
    SpecificationMapper,
)
from plantapop.shared.infrastructure.repository.sqlalchemy_repository import (
    SQLAlchemyRepository,
)
from plantapop.shared.infrastructure.repository.sqlalchemy_uow import (
    SQLAlchemyUnitOfWork,
)


class SQLRefreshToken(Base):
    __tablename__ = "refresh_tokens"

    uuid = Column(Uuid, primary_key=True)
    token = Column(String, nullable=False, unique=True)
    user_uuid = Column(Uuid, nullable=False)
    device = Column(String, nullable=False)
    expiration_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    revoked = Column(Boolean, default=False)


class TokenDataMapper(DataMapper[Token, SQLRefreshToken]):
    def model_to_entity(self, instance: SQLRefreshToken) -> Token:
        return Token(
            uuid=instance.uuid,  # type: ignore
            token=str(instance.token),
            token_type="refresh",
            user_uuid=instance.user_uuid,  # type: ignore
            device=str(instance.device),
            exp=instance.expiration_date,  # type: ignore
            revoked=bool(instance.revoked),
        )

    def entity_to_model(self, entity: Token) -> SQLRefreshToken:
        return SQLRefreshToken(
            uuid=entity.uuid,
            token=entity.token,
            user_uuid=entity.user_uuid,
            device=entity.device,
            expiration_date=entity.exp,
            revoked=entity.revoked,
        )


class RefreshJwtTokenRepository(SQLAlchemyRepository[Token]):
    mapper = TokenDataMapper()
    model = SQLRefreshToken
    specification_mapper = SpecificationMapper(
        {
            "token": SQLRefreshToken.token,
            "user_uuid": SQLRefreshToken.user_uuid,
            "device": SQLRefreshToken.device,
            "exp": SQLRefreshToken.expiration_date,
            "revoked": SQLRefreshToken.revoked,
        }
    )


class RefreshTokenUoW(SQLAlchemyUnitOfWork):
    repository = RefreshJwtTokenRepository
