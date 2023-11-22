import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

from plantapop import create_app
from plantapop.config import Config
from plantapop.shared.infrastructure.repository.database import Base

app = create_app()

config = Config.get_instance()
engine = sa.create_engine(config.postgres.url, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Set up the database once
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture()
def client():
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
        with app.session.session.override(session):
            yield TestClient(app)

    finally:
        if session.is_active:
            session.close()

        transaction.rollback()
        connection.close()
