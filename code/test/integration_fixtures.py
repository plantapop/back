import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from plantapop import get_base
from plantapop.shared.infrastructure.container import SessionContainer

Base = get_base()

engine = create_engine("sqlite:///:memory:", echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


container = SessionContainer()


@pytest.fixture
def i_session():
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
        with container.session.override(session):
            yield session

    finally:
        if session.is_active:
            session.close()

        transaction.rollback()
        connection.close()
