import asyncio

import pytest
import pytest_asyncio
from sqlalchemy import Column, Integer, String, event, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from plantapop import get_base
from plantapop.shared.infrastructure.container import SessionContainer

Base = get_base()


class Test(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)
    name = Column(String)


engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


container = SessionContainer()

asyncio.run(init_models())


@pytest_asyncio.fixture
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


@pytest_asyncio.fixture
async def session(connection_and_session):
    session, conn = connection_and_session
    yield session


@pytest.mark.asyncio
@pytest.mark.integration
async def test_session(session):
    test = Test(name="test")
    session.add(test)
    await session.commit()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_session_is_empty(session):
    objects = await session.execute(select(Test))
    assert len(objects.scalars().all()) == 0
