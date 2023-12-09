from typing import Type

from aio_pika import Message
from aio_pika.pool import Pool
from dependency_injector.wiring import Provide, inject

from plantapop.config import Config
from plantapop.shared.domain.event.domain_event import DomainEvent
from plantapop.shared.domain.event.event_subscriber import EventSubscriber
from plantapop.shared.domain.event.handler import Handler

config = Config.get_instance()


class PikaSubscriber(EventSubscriber):
    exchange_name: str
    binding_key: str
    handler: Type[Handler]
    event: Type[DomainEvent]

    @inject
    def __init__(self, chanel_pool: Pool = Provide["channel"]) -> None:
        self._chanel_pool = chanel_pool

    async def subscribe(self) -> None:
        async with self._chanel_pool.acquire() as channel:
            exchange = await channel.declare_exchange(self.exchange_name, type="topic")
            queue = await channel.declare_queue(exclusive=True)
            await queue.bind(exchange, routing_key=self.binding_key)
            await queue.consume(self.handle_event)

    async def handle_event(self, message: Message) -> None:
        try:
            await self.handle(message.body)
            await message.ack()
        except Exception:
            await self.handle_consumption_error(message)

    async def handle_consumption_error(self, message: Message) -> None:
        if message.headers.get("x-max-retry-count") > config.rabbitmq.max_retries:
            await self.send_to_dead_letter(message)
        else:
            await self.send_to_requeue(message)

    async def send_to_dead_letter(self, message: Message) -> None:
        async with self._chanel_pool.acquire() as channel:
            exchange = await channel.declare_exchange(
                "dead_letter_exchange", type="topic"
            )
            await exchange.publish(message, routing_key=message.routing_key)
            await message.ack()

    async def send_to_requeue(self, message: Message) -> None:
        message.headers["x-max-retry-count"] += 1
        async with self._chanel_pool.acquire() as channel:
            exchange = await channel.declare_exchange(self.exchange_name, type="topic")
            await exchange.publish(message, routing_key=message.routing_key)
            await message.ack()

    async def handle(self, payload: bytes) -> None:
        handler = self.handler()
        await handler.handle(DomainEvent.from_json(payload))
