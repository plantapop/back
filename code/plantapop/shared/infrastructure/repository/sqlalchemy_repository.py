from typing import Dict, List, Type
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from plantapop.shared.domain.repositories import GenericRepository, TEntity
from plantapop.shared.domain.specification.specification import Specification
from plantapop.shared.infrastructure.repository.data_mapper import DataMapper
from plantapop.shared.infrastructure.repository.database import Base
from plantapop.shared.infrastructure.repository.specification_mapper import (
    SpecificationMapper,
)

TBase = Type[Base]


class SQLAlchemyRepository(GenericRepository[TEntity]):
    specification_mapper: SpecificationMapper
    mapper: DataMapper
    model: TBase

    def __init__(
        self,
        db_session: AsyncSession,
        identity_map: Dict[UUID, TEntity] | None = None,
    ):
        self._session = db_session
        self.identity_map = identity_map or dict()

    async def get(self, uuid: UUID) -> TEntity | None:
        if uuid in self.identity_map:
            return self.identity_map[uuid]
        else:
            model = await self._get_model(uuid)
            if not model:
                return None
            entity = self.mapper.model_to_entity(model)
            return entity

    async def _get_model(self, uuid: UUID) -> TBase | None:
        return await self._session.get(self.model, uuid)

    async def count(self, spec: Specification | None = None) -> int:
        query = select(func.count()).select_from(self.model)
        if spec:
            query = self.specification_mapper.apply(query, spec)
        count = await self._session.execute(query)
        count_value = count.scalar()
        return int(count_value) if count_value is not None else 0

    async def save(self, entity: TEntity) -> None:
        model = self.mapper.entity_to_model(entity)
        self._session.add(model)
        self.identity_map[entity.uuid] = entity

    async def save_all(self, entities: List[TEntity]) -> None:
        for entity in entities:
            await self.save(entity)

    async def update(self, entity: TEntity) -> None:
        model = self.mapper.entity_to_model(entity)
        await self._session.merge(model)
        self.identity_map[entity.uuid] = entity

    async def blocking_update(self, entity: TEntity) -> None:
        db_model = await self._session.get(self.model, entity.uuid).with_for_update()  # type: ignore # noqa
        model = self.mapper.entity_to_model(entity)

        if db_model.version == model.version:
            raise ValueError("You Should Update Aggregate version before commit")

        if db_model.version != model.version - 1:
            raise ValueError("Entity has been modified by another process")

        await self._session.merge(model)
        self.identity_map[entity.uuid] = entity

    async def update_all(self, entities: List[TEntity]) -> None:
        for entity in entities:
            await self.update(entity)

    async def delete(self, entity: TEntity) -> None:
        model = await self._get_model(entity.uuid)
        await self._session.delete(model)
        self._remove_from_identity_map(entity)

    async def delete_all(self, entities: List[TEntity]) -> None:
        for entity in entities:
            await self.delete(entity)

    def _remove_from_identity_map(self, entity: TEntity) -> None:
        if entity.uuid in self.identity_map:
            del self.identity_map[entity.uuid]

    async def exists(
        self, uuid: UUID | None = None, spec: Specification | None = None
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

    async def matching(self, spec: Specification) -> List[TEntity]:
        query = select(self.model)
        query = self.specification_mapper.apply(query, spec)
        result = await self._session.execute(query)
        models = result.scalars().all()
        entities = [self._map_model_to_entity(model) for model in models]
        return entities

    def _map_model_to_entity(self, model) -> TEntity:
        entity = self.mapper.model_to_entity(model)
        self.identity_map[entity.uuid] = entity
        return entity

    async def commit(self) -> None:
        await self._session.commit()
