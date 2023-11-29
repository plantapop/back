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
        self._session = db_session  # type: _asyncio.Task

    async def __aenter__(self) -> SQLAlchemyRepository:
        if not isinstance(self._session, AsyncSession):  # if multiple time enter
            self._session = await self._session

        if isinstance(self.repo, type):
            self.repo = self.repo(self._session)

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
