from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from plantapop.shared.domain.entities import Entity
from plantapop.shared.infrastructure.repository.database import Base

MapperEntity = TypeVar("MapperEntity", bound=Entity)
MapperModel = TypeVar("MapperModel", bound=Base)


class DataMapper(Generic[MapperEntity, MapperModel], ABC):
    entity_class: MapperEntity
    model_class: MapperModel

    @abstractmethod
    def model_to_entity(self, instance: MapperModel) -> MapperEntity:
        raise NotImplementedError

    @abstractmethod
    def entity_to_model(self, entity: MapperEntity) -> MapperModel:
        raise NotImplementedError
