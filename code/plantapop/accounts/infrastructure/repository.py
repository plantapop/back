from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String, Uuid

from plantapop.accounts.domain.user import User
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


class SQLUser(Base):
    __tablename__ = "account_users"

    uuid = Column(Uuid, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surnames = Column(String, nullable=False)
    timezone = Column(String, nullable=False)
    language = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    active = Column(Boolean, nullable=False)
    verified = Column(Boolean, nullable=False)


class UserDataMapper(DataMapper[User, SQLUser]):
    def model_to_entity(self, instance: SQLUser) -> User:
        return User(
            uuid=instance.uuid,  # type: ignore
            email=str(instance.email),
            password=bytes(instance.password, "utf-8"),  # type: ignore
            name=str(instance.name),
            surnames=instance.surnames.split(" "),
            timezone=str(instance.timezone),
            language=instance.language.split(" "),
            created_at=instance.created_at,  # type: ignore
            updated_at=instance.updated_at,  # type: ignore
            active=bool(instance.active),
            verified=bool(instance.verified),
        )

    def entity_to_model(self, entity: User) -> SQLUser:
        return SQLUser(
            uuid=entity.uuid,
            email=entity.email,
            password=str(entity.password, "utf-8"),
            name=entity.name,
            surnames=" ".join(entity.surnames),
            timezone=entity.timezone,
            language=" ".join(entity.language),
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            active=entity.active,
            verified=entity.verified,
        )


class SqlUserRepository(SQLAlchemyRepository[User]):
    mapper = UserDataMapper()
    model = SQLUser
    specification_mapper = SpecificationMapper(
        {
            "uuid": SQLUser.uuid,
            "email": SQLUser.email,
            "password": SQLUser.password,
            "name": SQLUser.name,
            # "surnames": SqlUser.surnames,
            "timezone": SQLUser.timezone,
            # "language": SqlUser.language,
            "created_at": SQLUser.created_at,
            "updated_at": SQLUser.updated_at,
            "active": SQLUser.active,
            "verified": SQLUser.verified,
        }
    )


class SqlUserUnitOfWork(SQLAlchemyUnitOfWork):
    repository = SqlUserRepository
