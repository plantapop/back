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

    async def get(self, uuid: GenericUUID) -> Entity:
        return self._db.get(uuid)

    async def save(self, entity: Entity) -> None:
        self._db[entity.uuid] = entity

    async def save_all(self, entities: list[Entity]) -> None:
        for entity in entities:
            await self.save(entity)

    async def delete(self, entity: Entity) -> None:
        if entity.uuid in self._db:
            del self._db[entity.uuid]

    async def delete_all(self, entities: list[Entity]) -> None:
        for entity in entities:
            await self.delete(entity)

    async def exists(self, uuid: GenericUUID) -> bool:
        return uuid in self._db

    async def matching(self, specification: Specification) -> list[Entity]:
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

    async def count(self, specification: Specification = None) -> int:
        if specification:
            return len(await self.matching(specification))
        return len(self._db)

    async def update(self, entity: Entity) -> None:
        if entity.uuid in self._db:
            self._db[entity.uuid] = entity

    async def update_all(self, entities: list[Entity]) -> None:
        for entity in entities:
            await self.update(entity)

    async def commit(self) -> None:
        pass


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.repo = FakeRepository()

    async def __aenter__(self) -> FakeRepository:
        return self.repo

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def close(self):
        pass


class FakeEventBus:
    def __init__(self) -> None:
        self.publish_called = False
        self.events = []

    async def publish(self, events: list[dict]) -> None:
        self.publish_called = True
        self.events.extend(events)


@pytest.fixture
def unit_of_work():
    return FakeUnitOfWork()


@pytest.fixture
def event_bus():
    return FakeEventBus()
