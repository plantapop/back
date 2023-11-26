from typing import Dict, List, Type, TypeVar

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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
    mapper: DataMapper[DomainEntity, Base]
    model: Type[Base]

    def __init__(
        self,
        db_session: AsyncSession,
        identity_map: Dict[GenericUUID, DomainEntity] = None,
    ):
        self._session = db_session
        self.identity_map = identity_map or dict()

    async def get(self, uuid: GenericUUID) -> Entity:
        if uuid in self.identity_map:
            return self.identity_map[uuid]
        else:
            model = await self._get_model(uuid)
            if not model:
                return None
            entity = self.mapper.model_to_entity(model)
            return entity

    async def _get_model(self, uuid: GenericUUID) -> Base:
        return await self._session.get(self.model, uuid.get())

    async def count(self, specification: Specification = None) -> int:
        query = select(func.count()).select_from(self.model)
        if specification:
            query = self.specification_mapper.apply(query, specification)
        count = await self._session.execute(query)
        return count.scalar()

    async def save(self, entity: Entity) -> None:
        model = self.mapper.entity_to_model(entity)
        self._session.add(model)
        self.identity_map[entity.uuid] = entity

    async def save_all(self, entities: List[Entity]) -> None:
        for entity in entities:
            await self.save(entity)

    async def update(self, entity: Entity) -> None:
        model = self.mapper.entity_to_model(entity)
        self._session.merge(model)
        self.identity_map[entity.uuid] = entity

    async def update_all(self, entities: List[Entity]) -> None:
        for entity in entities:
            await self.update(entity)

    async def delete(self, entity: Entity) -> None:
        model = await self._get_model(entity.uuid)
        self._session.delete(model)
        self._remove_from_identity_map(entity)

    async def delete_all(self, entities: List[Entity]) -> None:
        for entity in entities:
            await self.delete(entity)

    def _remove_from_identity_map(self, entity: Entity) -> None:
        if entity.uuid in self.identity_map:
            del self.identity_map[entity.uuid]

    async def exists(
        self, uuid: GenericUUID = None, spec: Specification = None
    ) -> bool:
        if uuid:
            if uuid in self.identity_map:
                return True
            return await self._get_model(uuid) is not None

        if spec:
            query = select(self.model)
            query = self.specification_mapper.apply(query, spec)
            # get first result
            first = await self._session.execute(query)
            return first.scalar() is not None

        raise ValueError("uuid or specification must be provided")

    async def matching(self, spec: Specification) -> List[Entity]:
        query = select(self.model)
        query = self.specification_mapper.apply(query, spec)
        models = await self._session.execute(query)
        models = models.scalars().all()
        entities = [self._map_model_to_entity(model) for model in models]
        return entities

    def _map_model_to_entity(self, model: Base) -> Entity:
        entity = self.mapper.model_to_entity(model)
        self.identity_map[entity.uuid] = entity
        return entity

    async def commit(self) -> None:
        await self._session.commit()
