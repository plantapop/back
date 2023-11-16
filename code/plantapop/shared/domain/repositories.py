from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from plantapop.shared.domain.entities import Entity as DomainEntity
from plantapop.shared.domain.value_objects import GenericUUID

Entity = TypeVar("Entity", bound=DomainEntity)
EntityUUID = TypeVar("EntityUUID", bound=GenericUUID)


class GenericRepository(Generic[EntityUUID, Entity], metaclass=ABCMeta):
    @abstractmethod
    def get(self, uuid: GenericUUID) -> Entity:
        pass

    @abstractmethod
    def get_all(self) -> list[Entity]:
        pass

    @abstractmethod
    def add(self, entity: Entity) -> None:
        pass

    @abstractmethod
    def update(self, entity: Entity) -> None:
        pass

    @abstractmethod
    def delete(self, entity: Entity) -> None:
        pass
