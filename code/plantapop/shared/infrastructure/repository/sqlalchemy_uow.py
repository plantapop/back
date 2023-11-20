from typing import Type

from dependency_injector.wiring import Provide, inject

from plantapop.shared.domain.unit_of_work import UnitOfWork
from plantapop.shared.infrastructure.repository.sqlalchemy_repository import (
    SQLAlchemyRepository,
)


class SQLAlchemyUnitOfWork(UnitOfWork):
    repo = Type[SQLAlchemyRepository]

    @inject
    def __init__(self, db_session=Provide["session"]):
        self._session = db_session
        self.repo = self.repo(self._session)

    def __enter__(self) -> SQLAlchemyRepository:
        return self.repo

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    def commit(self):
        self.repo.commit()

    def rollback(self):
        self._session.rollback()

    def close(self):
        self._session.close()
