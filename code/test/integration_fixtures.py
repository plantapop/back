import asyncio
from test.conftest import init_models

import pytest
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from plantapop.shared.infrastructure.container import SessionContainer

engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

container = SessionContainer()

asyncio.run(init_models(engine))


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def connection_and_session():
    conn = await engine.connect()
    trans = await conn.begin()
    session = AsyncSession(bind=conn)

    await conn.begin_nested()

    @event.listens_for(session.sync_session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    with container.session.override(session):
        yield session, conn

    await session.close()
    await trans.rollback()
    await conn.close()


@pytest.fixture
async def session(connection_and_session):
    session, conn = connection_and_session
    yield session
