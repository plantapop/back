from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from plantapop.shared.domain.entities import Entity as DomainEntity
from plantapop.shared.domain.specification.specification import Specification
from plantapop.shared.domain.value_objects import GenericUUID

Entity = TypeVar("Entity", bound=DomainEntity)
EntityUUID = TypeVar("EntityUUID", bound=GenericUUID)


class GenericRepository(Generic[EntityUUID, Entity], metaclass=ABCMeta):
    @abstractmethod
    def get(self, uuid: GenericUUID) -> Entity:
        pass

    @abstractmethod
    def save(self, entity: Entity) -> None:
        pass

    @abstractmethod
    def save_all(self, entities: list[Entity]) -> None:
        pass

    @abstractmethod
    def delete(self, entity: Entity) -> None:
        pass

    @abstractmethod
    def exists(self, uuid: GenericUUID) -> bool:
        pass

    @abstractmethod
    def matching(self, specification: Specification) -> list[Entity]:
        pass
