from dependency_injector.wiring import Provide, inject
from sqlalchemy import Column, DateTime, String, Text, Uuid
from sqlalchemy.ext.asyncio import AsyncSession

from plantapop.shared.domain.event.domain_event import DomainEvent
from plantapop.shared.domain.event.event_bus import EventBus
from plantapop.shared.infrastructure.repository.database import Base


class SQLDomainEvent(Base):
    __tablename__ = "domain_events"

    event_uuid = Column(Uuid, nullable=False, primary_key=True)
    event_name = Column(String(255), nullable=False)
    aggregate_uuid = Column(Uuid, nullable=False)
    event_body = Column(Text, nullable=False)
    occurred_on = Column(DateTime, nullable=False)
    exchange_name = Column(String(255), nullable=False)
    topic_name = Column(String(255), nullable=False)


class SqlAlchemyFailoverEventBus(EventBus):
    exchange_name: str

    @inject
    def __init__(
        self, exchange_name: str, db_session: AsyncSession = Provide["session"]
    ):
        self._session = db_session
        self.exchange_name = exchange_name

    async def publish(self, events: list[DomainEvent]) -> None:
        async with self._session.begin():
            self._session.add_all(
                [
                    SQLDomainEvent(
                        event_uuid=event.event_uuid,
                        event_name=event.event_name,
                        aggregate_uuid=event.aggregate_uuid,
                        event_body=event.event_body,
                        occurred_on=event.occurred_on,
                        exchange_name=self.exchange_name,
                        topic_name=event.event_name,
                    )
                    for event in events
                ]
            )
            await self._session.commit()
