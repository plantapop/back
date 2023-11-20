import pytest
import sqlalchemy as sa
import toml
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

from plantapop import app
from plantapop.config import Config
from plantapop.shared.infrastructure.repository.database import Base

config = Config.get_instance()

try:
    engine = sa.create_engine(config.postgres.url, echo=True)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Set up the database once
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    @pytest.fixture()
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

    @pytest.fixture()
    def client(session):
        with app.session.session.override(session):
            yield TestClient(app)

except Exception as e:
    print(f"No database available: Only unittest or integration can be run: {e}")


@pytest.fixture()
def app_version():
    """Get App version from pyproject.toml"""

    with open("pyproject.toml", "r") as f:
        pyproject = toml.load(f)
    return pyproject["tool"]["poetry"]["version"]
