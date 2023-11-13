from shared_kernel.domain.entities import Entity
from shared_kernel.domain.exceptions import EntityNotFoundException
from shared_kernel.domain.repositories import GenericRepository
from shared_kernel.domain.value_objects import GenericUUID
from shared_kernel.infrastructure.data_mapper import DataMapper
from sqlalchemy.orm import DeclarativeBase, Session


class Removed:
    def __repr__(self):
        return "<Removed entity>"

    def __str__(self):
        return "<Removed entity>"


REMOVED = Removed()


class SqlAlchemyGenericRepository(GenericRepository[GenericUUID, Entity]):
    mapper_class: type[DataMapper[Entity, DeclarativeBase]]
    model_class: type[Entity]

    def __init__(self, db_session: Session, identity_map=None):
        self._session = db_session
        self._identity_map = identity_map or dict()

    def add(self, entity: Entity):
        self._identity_map[entity.uuid] = entity
        instance = self.map_entity_to_model(entity)
        self._session.add(instance)

    def remove(self, entity: Entity):
        self._check_not_removed(entity.uuid)
        self._identity_map[entity.uuid] = REMOVED
        instance = self._session.query(self.get_model_class()).get(entity.uuid)
        self._session.delete(instance)

    def remove_by_id(self, entity_uuid: GenericUUID):
        self._check_not_removed(entity_uuid)
        self._identity_map[entity_uuid] = REMOVED
        instance = self._session.query(self.get_model_class()).get(entity_uuid)
        if instance is None:
            raise EntityNotFoundException(
                repository=self, entity_uuid=entity_uuid)
        self._session.delete(instance)

    def get_by_id(self, entity_uuid: GenericUUID):
        instance = self._session.query(self.get_model_class()).get(entity_uuid)
        if instance is None:
            raise EntityNotFoundException(
                repository=self, entity_uuid=entity_uuid)
        return self._get_entity(instance)

    def persist(self, entity: Entity):
        self._check_not_removed(entity.uuid)
        assert (
            entity.uuid in self._identity_map
        ), """Cannon persist entity which is unknown to the repo.
        Did you forget to call repo.add() for this entity?"""
        instance = self.map_entity_to_model(entity)
        merged = self._session.merge(instance)
        self._session.add(merged)

    def persist_all(self):
        for entity in self._identity_map.values():
            if entity is not REMOVED:
                self.persist(entity)

    def collect_events(self):
        events = []
        for entity in self._identity_map.values():
            if entity is not REMOVED:
                events.extend(entity.collect_events())
        return events

    @property
    def data_mapper(self):
        return self.mapper_class()

    def count(self) -> int:
        return self._session.query(self.model_class).count()

    def map_entity_to_model(self, entity: Entity):
        assert self.mapper_class, (
            f"No data_mapper attribute in {self.__class__.__name__}. "
            """Make sure to include `mapper_class = MyDataMapper`
            in the Repository class."""
        )

        return self.data_mapper.entity_to_model(entity)

    def map_model_to_entity(self, instance) -> Entity:
        assert self.data_mapper
        return self.data_mapper.model_to_entity(instance)

    def get_model_class(self):
        assert self.model_class is not None, (
            f"No model_class attribute in in {self.__class__.__name__}. "
            "Make sure to include `model_class = MyModel` in the class."
        )
        return self.model_class

    def _get_entity(self, instance):
        if instance is None:
            return None
        entity = self.map_model_to_entity(instance)
        self._check_not_removed(entity.uuid)

        if entity.uuid in self._identity_map:
            return self._identity_map[entity.uuid]

        self._identity_map[entity.uuid] = entity
        return entity

    def _check_not_removed(self, entity_uuid):
        assert (
            self._identity_map.get(entity_uuid, None) is not REMOVED
        ), f"Entity {entity_uuid} already removed"
