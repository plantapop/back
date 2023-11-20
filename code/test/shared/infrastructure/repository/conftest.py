import uuid

import pytest
from sqlalchemy import Column, Integer, String, Uuid, create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

from plantapop.shared.domain.value_objects import GenericUUID
from plantapop.shared.infrastructure.repository.data_mapper import DataMapper
from plantapop.shared.infrastructure.repository.sqlalchemy_uow import (
    SQLAlchemyUnitOfWork,
)

Base = declarative_base()


class DomainTestBase:
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


class TestBaseDataMapper(DataMapper[DomainTestBase, AlchemyBase]):
    @classmethod
    def entity_to_model(cls, entity: DomainTestBase) -> AlchemyBase:
        return AlchemyBase(
            uuid=entity.uuid.get(),
            table_name=entity.name,
            table_age=entity.age,
            table_email=entity.email,
        )

    @classmethod
    def model_to_entity(cls, model: AlchemyBase) -> DomainTestBase:
        return DomainTestBase(
            uuid=model.uuid,
            name=model.table_name,
            age=model.table_age,
            email=model.table_email,
        )


engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


MAP = {
    "uuid": "uuid",
    "name": "table_name",
    "age": "table_age",
    "email": "table_email",
}


@pytest.fixture
def _session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(sess, trans):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    if session.is_active:
        session.close()

    transaction.rollback()
    connection.close()


class SqlTestUoW(SQLAlchemyUnitOfWork):
    repo = TestBaseDataMapper


@pytest.fixture
def john_doe():
    return DomainTestBase(uuid=uuid.uuid4(), name="John", age=25, email="gmail")


@pytest.fixture
def jane_doe():
    return DomainTestBase(uuid=uuid.uuid4(), name="Jane", age=20, email="gmail")


@pytest.fixture
def john_smith():
    return DomainTestBase(uuid=uuid.uuid4(), name="John", age=30, email="hotmail")


@pytest.fixture
def jane_smith():
    return DomainTestBase(uuid=uuid.uuid4(), name="Jane", age=35, email="hotmail")


@pytest.fixture
def session(_session, john_doe, jane_doe, john_smith, jane_smith):
    _session.add_all(
        [
            TestBaseDataMapper.entity_to_model(john_doe),
            TestBaseDataMapper.entity_to_model(jane_doe),
            TestBaseDataMapper.entity_to_model(john_smith),
            TestBaseDataMapper.entity_to_model(jane_smith),
        ]
    )

    _session.commit()

    return _session
