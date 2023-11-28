import logging

from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base

from plantapop.config import Config

config = Config.get_instance()
logger = logging.getLogger(__name__)

Base = declarative_base()

engine = create_async_engine(config.postgres.url, echo=False)

SessionLocal = orm.sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
