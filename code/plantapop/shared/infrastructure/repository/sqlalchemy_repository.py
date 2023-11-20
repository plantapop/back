from typing import Dict, List, Type, TypeVar

from sqlalchemy.orm import Session

from plantapop.shared.domain.entities import Entity as DomainEntity
from plantapop.shared.domain.repositories import GenericRepository
from plantapop.shared.domain.specification.specification import Specification
from plantapop.shared.domain.value_objects import GenericUUID
from plantapop.shared.infrastructure.repository.data_mapper import DataMapper
from plantapop.shared.infrastructure.repository.database import Base
from plantapop.shared.infrastructure.repository.specification_mapper import (
    SpecificationMapper,
)

Entity = TypeVar("Entity", bound=DomainEntity)
EntityUUID = TypeVar("EntityUUID", bound=GenericUUID)


class SQLAlchemyRepository(GenericRepository):
    specification_mapper: SpecificationMapper
    mapper: Type[DataMapper[DomainEntity, Base]]
    model: Type[Base]

    def __init__(
        self, db_session: Session, identity_map: Dict[GenericUUID, DomainEntity] = None
    ):
        self._session = db_session
        self.identity_map = identity_map or dict()

    def get(self, uuid: GenericUUID) -> Entity:
        if uuid in self.identity_map:
            return self.identity_map[uuid]
        else:
            model = self._get_model(uuid)
            if not model:
                return None
            entity = self.mapper.model_to_entity(model)
            return entity

    def _get_model(self, uuid: GenericUUID) -> Base:
        return self._session.get(self.model, uuid.get())

    def count(self, specification: Specification = None) -> int:
        query = self._session.query(self.model)
        if specification:
            query = self.specification_mapper.apply(query, specification)
        return query.count()

    def save(self, entity: Entity) -> None:
        model = self.mapper.entity_to_model(entity)
        self._session.add(model)
        self.identity_map[entity.uuid] = entity

    def save_all(self, entities: List[Entity]) -> None:
        for entity in entities:
            self.save(entity)

    def update(self, entity: Entity) -> None:
        model = self.mapper.entity_to_model(entity)
        self._session.merge(model)
        self.identity_map[entity.uuid] = entity

    def update_all(self, entities: List[Entity]) -> None:
        for entity in entities:
            self.update(entity)

    def delete(self, entity: Entity) -> None:
        model = self._get_model(entity.uuid)
        self._session.delete(model)
        self._remove_from_identity_map(entity)

    def delete_all(self, entities: List[Entity]) -> None:
        for entity in entities:
            self.delete(entity)

    def _remove_from_identity_map(self, entity: Entity) -> None:
        if entity.uuid in self.identity_map:
            del self.identity_map[entity.uuid]

    def exists(self, uuid: GenericUUID = None, spec: Specification = None) -> bool:
        if uuid:
            if uuid in self.identity_map:
                return True
            return self._get_model(uuid) is not None

        if spec:
            query = self._session.query(self.model)
            query = self.specification_mapper.apply(query, spec)
            return query.first() is not None

        raise ValueError("uuid or specification must be provided")

    def matching(self, spec: Specification) -> List[Entity]:
        query = self._session.query(self.model)
        query = self.specification_mapper.apply(query, spec)
        models = query.all()
        entities = [self._map_model_to_entity(model) for model in models]
        return entities

    def _map_model_to_entity(self, model: Base) -> Entity:
        entity = self.mapper.model_to_entity(model)
        self.identity_map[entity.uuid] = entity
        return entity

    def commit(self) -> None:
        self._session.commit()
