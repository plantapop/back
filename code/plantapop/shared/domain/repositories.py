from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from plantapop.shared.domain.entities import Entity
from plantapop.shared.domain.specification.specification import Specification

TEntity = TypeVar("TEntity", bound=Entity)


class GenericRepository(Generic[TEntity], metaclass=ABCMeta):
    @abstractmethod
    async def get(self, uuid: UUID) -> TEntity | None:
        pass

    @abstractmethod
    async def save(self, entity: TEntity) -> None:
        pass

    @abstractmethod
    async def save_all(self, entities: list[TEntity]) -> None:
        pass

    @abstractmethod
    async def delete(self, entity: TEntity) -> None:
        pass

    @abstractmethod
    async def delete_all(self, entities: list[TEntity]) -> None:
        pass

    @abstractmethod
    async def exists(self, uuid: UUID) -> bool:
        pass

    @abstractmethod
    async def matching(self, spec: Specification) -> list[TEntity]:
        pass

    @abstractmethod
    async def count(self, spec: Specification | None = None) -> int:
        pass

    @abstractmethod
    async def update(self, entity: TEntity) -> None:
        pass

    @abstractmethod
    async def update_all(self, entities: list[TEntity]) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass
