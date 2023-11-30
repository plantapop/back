from typing import Type

from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import AsyncSession

from plantapop.shared.domain.unit_of_work import UnitOfWork
from plantapop.shared.infrastructure.repository.sqlalchemy_repository import (
    SQLAlchemyRepository,
)


class SQLAlchemyUnitOfWork(UnitOfWork):
    repository: Type[SQLAlchemyRepository]

    @inject
    async def __aenter__(
        self, db_session: AsyncSession = Provide["session"]
    ) -> SQLAlchemyRepository:
        self._session = db_session

        self.repo = self.repository(self._session)

        return self.repo

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

        await self.close()

    async def commit(self):
        try:
            await self._session.flush()
            await self._session.commit()

        except Exception:
            await self._session.rollback()

    async def rollback(self):
        await self._session.rollback()

    async def close(self):
        await self._session.close()
