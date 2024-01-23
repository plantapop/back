import logging
from typing import AsyncGenerator

from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from plantapop.config import Config

config = Config.get_instance()
logger = logging.getLogger(__name__)

Base = declarative_base()

engine = create_async_engine(config.postgres.url, echo=False, poolclass=NullPool)

SessionLocal = orm.sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,  # type: ignore
)


async def session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:  # type: ignore
        yield session
