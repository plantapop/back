from abc import ABC, abstractmethod
from typing import TypeVar

from plantapop.shared.domain.repositories import GenericRepository

U = TypeVar("U", bound="UnitOfWork")


class UnitOfWork(ABC):
    @abstractmethod
    def __enter__(self: U) -> GenericRepository:
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def close(self):
        pass
