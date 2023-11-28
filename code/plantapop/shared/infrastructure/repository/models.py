from sqlalchemy.ext.asyncio import AsyncEngine

from plantapop.shared.infrastructure.event.sqlalchemy_failover_event_bus import (
    SQLDomainEvent,
)
from plantapop.shared.infrastructure.repository.database import Base, engine
from plantapop.shared.infrastructure.token.token_repository import RefreshToken

all_models = [RefreshToken, SQLDomainEvent]


def get_base():
    return Base


async def init_models(engine: AsyncEngine = engine):
    Base = get_base()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
