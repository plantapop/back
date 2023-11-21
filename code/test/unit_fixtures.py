import pytest

from plantapop.shared.domain.entities import Entity
from plantapop.shared.domain.repositories import GenericRepository
from plantapop.shared.domain.specification.order import Order, OrderType
from plantapop.shared.domain.specification.specification import Specification
from plantapop.shared.domain.unit_of_work import UnitOfWork
from plantapop.shared.domain.value_objects import GenericUUID


class FakeRepository(GenericRepository):
    def __init__(self) -> None:
        self._db: dict[GenericUUID, Entity] = {}

    def get(self, uuid: GenericUUID) -> Entity:
        return self._db.get(uuid)

    def save(self, entity: Entity) -> None:
        self._db[entity.uuid] = entity

    def save_all(self, entities: list[Entity]) -> None:
        for entity in entities:
            self.save(entity)

    def delete(self, entity: Entity) -> None:
        if entity.uuid in self._db:
            del self._db[entity.uuid]

    def delete_all(self, entities: list[Entity]) -> None:
        for entity in entities:
            self.delete(entity)

    def exists(self, uuid: GenericUUID) -> bool:
        return uuid in self._db

    def matching(self, specification: Specification) -> list[Entity]:
        list_matching_filter = [
            entity
            for entity in self._db.values()
            if specification.is_satisfied_by(entity)
        ]

        if specification.order:
            list_matching_filter.sort(
                key=lambda entity: self._get_order_key(entity, specification.order)
            )

        if specification.offset:
            list_matching_filter = list_matching_filter[specification.offset :]

        if specification.limit:
            list_matching_filter = list_matching_filter[: specification.limit]

        return list_matching_filter

    def _get_order_key(self, entity: Entity, order: Order) -> object:
        field_value = getattr(entity, order.field)
        return field_value if order.order_type == OrderType.ASC else -field_value

    def count(self, specification: Specification = None) -> int:
        if specification:
            return len(self.matching(specification))
        return len(self._db)

    def update(self, entity: Entity) -> None:
        if entity.uuid in self._db:
            self._db[entity.uuid] = entity

    def update_all(self, entities: list[Entity]) -> None:
        for entity in entities:
            self.update(entity)

    def commit(self) -> None:
        pass


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.repo = FakeRepository()

    def __enter__(self) -> FakeRepository:
        return self.repo

    def __exit__(self, exc_type, exc_value, traceback):
        self.commit()

    def commit(self):
        self.repo.commit()

    def rollback(self):
        pass

    def close(self):
        pass


@pytest.fixture
def unit_of_work():
    return FakeUnitOfWork()
