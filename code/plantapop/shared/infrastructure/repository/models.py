from sqlalchemy.ext.asyncio import AsyncEngine

from plantapop.accounts.infrastructure.repository import SQLUser
from plantapop.shared.infrastructure.event.sqlalchemy_failover_event_bus import (
    SQLDomainEvent,
)
from plantapop.shared.infrastructure.repository.database import Base, engine
from plantapop.shared.infrastructure.token.token_repository import SQLRefreshToken

all_models = [SQLRefreshToken, SQLDomainEvent, SQLUser]


def get_base():
    return Base


async def init_models(engine: AsyncEngine = engine):
    Base = get_base()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
