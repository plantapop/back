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


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    uuid = Column(Uuid, nullable=False)
    token = Column(String, primary_key=True)
    user_uuid = Column(Uuid, nullable=False)
    device = Column(String, nullable=False)
    expiration_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    revoked = Column(Boolean, default=False)


class TokenDataMapper(DataMapper[Token, RefreshToken]):
    def model_to_entity(self, model: RefreshToken) -> Token:
        return Token(
            uuid=model.uuid,
            token=model.token,
            token_type="refresh",
            user_uuid=model.user_uuid,
            device=model.device,
            exp=model.expiration_date,
            revoked=model.revoked,
        )

    def entity_to_model(self, entity: Token) -> RefreshToken:
        return RefreshToken(
            uuid=entity.uuid,
            token=entity.token,
            user_uuid=entity.user_uuid,
            device=entity.device,
            expiration_date=entity.exp,
            revoked=entity.revoked,
        )


class RefreshJwtTokenRepository(SQLAlchemyRepository):
    mapper = TokenDataMapper()
    model = RefreshToken
    specification_mapper = SpecificationMapper(
        {
            "token": RefreshToken.token,
            "user_uuid": RefreshToken.user_uuid,
            "device": RefreshToken.device,
            "exp": RefreshToken.expiration_date,
            "revoked": RefreshToken.revoked,
        }
    )


class RefreshTokenUoW(SQLAlchemyUnitOfWork):
    repo = RefreshJwtTokenRepository
