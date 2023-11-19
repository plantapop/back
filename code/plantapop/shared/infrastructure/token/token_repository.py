from datetime import datetime
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from sqlalchemy import Boolean, Column, DateTime, String, Uuid
from sqlalchemy.orm.session import Session

from plantapop.shared.domain.token.token import Token
from plantapop.shared.domain.token.token_repository import TokenRepository
from plantapop.shared.infrastructure.repository.data_mapper import DataMapper
from plantapop.shared.infrastructure.repository.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token = Column(String, primary_key=True)
    user_uuid = Column(Uuid, nullable=False)
    device = Column(String, nullable=False)
    expiration_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    revoked = Column(Boolean, default=False)


class TokenDataMapper(DataMapper[Token, RefreshToken]):
    def model_to_entity(self, model: RefreshToken) -> Token:
        return Token(
            token=model.token,
            token_type="refresh",
            user_uuid=model.user_uuid,
            device=model.device,
            exp=model.expiration_date,
            revoked=model.revoked,
        )

    def entity_to_model(self, entity: Token) -> RefreshToken:
        return RefreshToken(
            token=entity.token,
            user_uuid=entity.user_uuid.get(),
            device=entity.device,
            expiration_date=entity.exp,
            revoked=entity.revoked,
        )


class RefreshJwtTokenRepository(TokenRepository):
    @inject
    def __init__(self, session: Session = Provide["session"]):
        self.session = session
        self.mapper = TokenDataMapper()
        self.model = RefreshToken

    def get(self, token: str) -> Token:
        entity = self.session.query(self.model).get(token)
        return self.mapper.model_to_entity(entity)

    def save(self, token: Token) -> None:
        entity = self.mapper.entity_to_model(token)
        self.session.add(entity)
        self.session.commit()

    def get_token_by_user_and_device(self, uuid: UUID, device: str) -> Token:
        try:
            entity = (
                self.session.query(self.model)
                .filter(self.model.user_uuid == uuid)
                .filter(self.model.device == device)
                .filter(self.model.revoked is False)
                .one()
            )
            return self.mapper.model_to_entity(entity)
        except Exception:
            return None

    def find_all_by_user(self, uuid: UUID) -> list[Token]:
        entities = self.session.query(self.model).filter(self.model.user_uuid == uuid)
        return [self.mapper.model_to_entity(entity) for entity in entities]

    def save_all(self, tokens: list[Token]) -> None:
        entities = [self.mapper.entity_to_model(token) for token in tokens]
        self.session.add_all(entities)
        self.session.commit()
