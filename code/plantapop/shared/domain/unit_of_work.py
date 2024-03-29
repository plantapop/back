from abc import ABC, abstractmethod

from plantapop.shared.domain.repositories import GenericRepository


class UnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self) -> GenericRepository:
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass

    @abstractmethod
    async def close(self):
        pass
