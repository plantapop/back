from aio_pika import Message
from aio_pika.pool import Pool
from dependency_injector.wiring import Provide, inject

from plantapop.shared.domain.event.domain_event import DomainEvent
from plantapop.shared.domain.event.event_bus import EventBus
from plantapop.shared.infrastructure.event.sqlalchemy_failover_event_bus import (
    SqlAlchemyFailoverEventBus,
)


class PikaEventBus(EventBus):
    exchange_name: str

    @inject
    def __init__(self, chanel_pool: Pool = Provide["channel"]) -> None:
        self._chanel_pool = chanel_pool
        self.failover = SqlAlchemyFailoverEventBus(self.exchange_name)

    async def publish(self, events: list[DomainEvent]) -> None:
        try:
            await self._publish(events)
        except Exception:
            await self.failover(events)

    async def _publish(self, events: list[DomainEvent]) -> None:
        async with self._chanel_pool.acquire() as channel:
            exchange = await channel.declare_exchange(self.exchange_name, type="topic")
            for event in events:
                message = Message(
                    event.to_json().encode("utf-8"),
                    content_type="application/json",
                    content_encoding="utf-8",
                )
                await exchange.publish(message, routing_key=event.event_name)

    async def failover(self, events: list[DomainEvent]) -> None:
        await self.failover.publish(events)
