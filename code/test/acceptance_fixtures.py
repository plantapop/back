import asyncio

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession

from plantapop.shared.infrastructure.controller.app import create_app
from plantapop.shared.infrastructure.repository.database import engine
from plantapop.shared.infrastructure.repository.models import init_models

none = asyncio.wait(init_models(engine))

app = create_app()


@pytest_asyncio.fixture
async def client(event_loop):
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
            yield AsyncClient(
                app=app, base_url="http://test"
            )  # creates new thread / loop for this client and it fails
        finally:
            await session.close()
            await trans.rollback()
            await conn.close()
