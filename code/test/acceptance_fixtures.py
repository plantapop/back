import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession

from plantapop.shared.infrastructure.controller.app import create_app
from plantapop.shared.infrastructure.repository.database import engine
from plantapop.shared.infrastructure.repository.models import init_models

app = create_app()


@app.on_event("startup")
async def startup_event():
    await init_models(engine)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client():
    conn = await engine.connect()
    trans = await conn.begin()
    session = AsyncSession(bind=conn)

    await conn.begin_nested()

    @event.listens_for(session.sync_session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    with app.session.session.override(session):
        try:
            async with AsyncClient(app=app, base_url="http://test") as client:
                print("Client is ready")
                yield client
        finally:
            await session.close()
            await trans.rollback()
            await conn.close()
