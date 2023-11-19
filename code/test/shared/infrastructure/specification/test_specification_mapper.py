import pytest
from sqlalchemy import Column, Integer, String, create_engine, event
from sqlalchemy.orm import Query, declarative_base, sessionmaker

from plantapop.shared.domain.specification.filter import (
    Contains,
    Equals,
    LessThan,
    NotEqual,
)
from plantapop.shared.domain.specification.specification import Specification
from plantapop.shared.infrastructure.repository.specification_mapper import (
    SpecificationMapper,
)

Base = declarative_base()


class DomainTestBase:
    id: int
    name: str
    age: int
    email: str

    def __init__(self, id: int, name: str, age: int, email: str):
        self.id = id
        self.name = name
        self.age = age
        self.email = email


class TestBase(Base):
    __tablename__ = "test_base"

    id = Column(Integer, primary_key=True)
    table_name = Column(String, nullable=False)
    table_age = Column(Integer, nullable=False)
    table_email = Column(String, nullable=False)


engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

Base.metadata.create_all(engine)

MAP = {
    "id": "id",
    "name": "table_name",
    "age": "table_age",
    "email": "table_email",
}


@pytest.fixture
def session():
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


@pytest.fixture
def john_doe():
    return DomainTestBase(id=1, name="John", age=25, email="gmail")


@pytest.fixture
def jane_doe():
    return DomainTestBase(id=2, name="Jane", age=20, email="gmail")


@pytest.fixture
def john_smith():
    return DomainTestBase(id=3, name="John", age=30, email="hotmail")


@pytest.fixture
def jane_smith():
    return DomainTestBase(id=4, name="Jane", age=35, email="hotmail")


@pytest.fixture
def database(session, john_doe, jane_doe, john_smith, jane_smith):
    session.add_all(
        [
            TestBase(
                id=john_doe.id,
                table_name=john_doe.name,
                table_age=john_doe.age,
                table_email=john_doe.email,
            ),
            TestBase(
                id=jane_doe.id,
                table_name=jane_doe.name,
                table_age=jane_doe.age,
                table_email=jane_doe.email,
            ),
            TestBase(
                id=john_smith.id,
                table_name=john_smith.name,
                table_age=john_smith.age,
                table_email=john_smith.email,
            ),
            TestBase(
                id=jane_smith.id,
                table_name=jane_smith.name,
                table_age=jane_smith.age,
                table_email=jane_smith.email,
            ),
        ]
    )

    session.commit()

    return session


@pytest.mark.integration
def test_specification_mapper_case_1(database, john_smith):
    # Given
    spec = Specification(filter=Equals("name", "John") & NotEqual("age", 25))

    # When
    mapper = SpecificationMapper(MAP)
    query: Query = mapper.run_specification(database.query(TestBase), spec).all()

    # Then
    assert len(query) == 1
    assert query[0].id == john_smith.id
    assert query[0].table_name == john_smith.name
    assert query[0].table_age == john_smith.age
    assert query[0].table_email == john_smith.email


@pytest.mark.integration
def test_specification_mapper_case_2(database, john_smith, jane_smith):
    # Given
    spec = Specification(
        filter=NotEqual("age", 25) & Equals("name", "John")
        | Contains("email", ["hotmail"])  # noqa
    )

    # When
    mapper = SpecificationMapper(MAP)
    query: Query = mapper.run_specification(database.query(TestBase), spec).all()

    # Then
    assert len(query) == 2
    assert query[0].id == john_smith.id
    assert query[0].table_name == john_smith.name
    assert query[0].table_age == john_smith.age
    assert query[0].table_email == john_smith.email
    assert query[1].id == jane_smith.id
    assert query[1].table_name == jane_smith.name
    assert query[1].table_age == jane_smith.age
    assert query[1].table_email == jane_smith.email


@pytest.mark.integration
def test_specification_mapper_case_3(database):
    # Given

    spec = Specification(
        filter=Equals("name", "John")
        | (NotEqual("age", 25) | (Contains("email", ["hotmail"]) & LessThan("age", 35)))  # noqa
    )

    # When
    mapper = SpecificationMapper(MAP)
    query: Query = mapper.run_specification(database.query(TestBase), spec).all()

    # Then
    assert len(query) == 4
