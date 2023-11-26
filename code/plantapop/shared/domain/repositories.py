from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from plantapop.shared.domain.entities import Entity as DomainEntity
from plantapop.shared.domain.specification.specification import Specification
from plantapop.shared.domain.value_objects import GenericUUID

Entity = TypeVar("Entity", bound=DomainEntity)
EntityUUID = TypeVar("EntityUUID", bound=GenericUUID)


class GenericRepository(Generic[EntityUUID, Entity], metaclass=ABCMeta):
    @abstractmethod
    async def get(self, uuid: GenericUUID) -> Entity:
        pass

    @abstractmethod
    async def save(self, entity: Entity) -> None:
        pass

    @abstractmethod
    async def save_all(self, entities: list[Entity]) -> None:
        pass

    @abstractmethod
    async def delete(self, entity: Entity) -> None:
        pass

    @abstractmethod
    async def delete_all(self, entities: list[Entity]) -> None:
        pass

    @abstractmethod
    async def exists(self, uuid: GenericUUID) -> bool:
        pass

    @abstractmethod
    async def matching(self, specification: Specification) -> list[Entity]:
        pass

    @abstractmethod
    async def count(self, specification: Specification = None) -> int:
        pass

    @abstractmethod
    async def update(self, entity: Entity) -> None:
        pass

    @abstractmethod
    async def update_all(self, entities: list[Entity]) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass
