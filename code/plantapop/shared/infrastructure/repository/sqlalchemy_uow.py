from typing import Type

from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import AsyncSession

from plantapop.shared.domain.unit_of_work import UnitOfWork
from plantapop.shared.infrastructure.repository.sqlalchemy_repository import (
    SQLAlchemyRepository,
)


class SQLAlchemyUnitOfWork(UnitOfWork):
    repo = Type[SQLAlchemyRepository]

    @inject
    def __init__(self, db_session: AsyncSession = Provide["session"]):
        # https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession.begin
        self._session = db_session
        self.repo = self.repo(self._session)

    async def __aenter__(self) -> SQLAlchemyRepository:
        return self.repo

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

        await self.close()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def close(self):
        await self._session.close()
