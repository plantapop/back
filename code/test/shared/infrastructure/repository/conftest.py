import uuid

import pytest
import pytest_asyncio
from sqlalchemy import Column, Integer, String, Uuid, select
from sqlalchemy.orm import declarative_base

from plantapop.shared.domain.value_objects import GenericUUID
from plantapop.shared.infrastructure.repository.data_mapper import DataMapper

Base = declarative_base()


class DomainBase:
    uuid: int
    name: str
    age: int
    email: str

    def __init__(self, uuid: uuid.UUID, name: str, age: int, email: str):
        self.uuid = GenericUUID(uuid)
        self.name = name
        self.age = age
        self.email = email


class AlchemyBase(Base):
    __tablename__ = "test_base"

    uuid = Column(Uuid, primary_key=True)
    table_name = Column(String, nullable=False)
    table_age = Column(Integer, nullable=False)
    table_email = Column(String, nullable=False)


class TestBaseDataMapper(DataMapper[DomainBase, AlchemyBase]):
    @classmethod
    def entity_to_model(cls, entity: DomainBase) -> AlchemyBase:
        return AlchemyBase(
            uuid=entity.uuid.get(),
            table_name=entity.name,
            table_age=entity.age,
            table_email=entity.email,
        )

    @classmethod
    def model_to_entity(cls, model: AlchemyBase) -> DomainBase:
        return DomainBase(
            uuid=model.uuid,
            name=model.table_name,
            age=model.table_age,
            email=model.table_email,
        )


MAP = {
    "uuid": AlchemyBase.uuid,
    "name": AlchemyBase.table_name,
    "age": AlchemyBase.table_age,
    "email": AlchemyBase.table_email
}


@pytest.fixture
def john_doe():
    return DomainBase(uuid=uuid.uuid4(), name="John", age=25, email="gmail")


@pytest.fixture
def jane_doe():
    return DomainBase(uuid=uuid.uuid4(), name="Jane", age=20, email="gmail")


@pytest.fixture
def john_smith():
    return DomainBase(uuid=uuid.uuid4(), name="John", age=30, email="hotmail")


@pytest.fixture
def jane_smith():
    return DomainBase(uuid=uuid.uuid4(), name="Jane", age=35, email="hotmail")


# Override the session fixture from test/integration_fixtures.py to add the test data
@pytest_asyncio.fixture
async def asession(connection_and_session, john_doe, jane_doe, john_smith, jane_smith):
    session, conn = connection_and_session
    await conn.run_sync(Base.metadata.create_all)
    session.add_all(
        [
            TestBaseDataMapper.entity_to_model(john_doe),
            TestBaseDataMapper.entity_to_model(jane_doe),
            TestBaseDataMapper.entity_to_model(john_smith),
            TestBaseDataMapper.entity_to_model(jane_smith),
        ]
    )

    await session.commit()
    yield session



