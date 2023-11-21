import pytest
from dependency_injector import containers, providers
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from plantapop import get_base
from plantapop.shared.infrastructure.repository import sqlalchemy_uow

Base = get_base()

engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


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

    try:
        yield session

    finally:
        if session.is_active:
            session.close()

        transaction.rollback()
        connection.close()


@pytest.fixture
def session():
    yield from _session()


class SessionFactory(providers.Factory):
    def __init__(self):
        super().__init__(_session)


class IntegrationTestContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[sqlalchemy_uow])

    session = providers.Resource(_session)


intefration_container = IntegrationTestContainer()


@pytest.fixture
def container():
    return intefration_container


@pytest.fixture
def isolated(container, session):
    with container.session.override(session):
        yield
