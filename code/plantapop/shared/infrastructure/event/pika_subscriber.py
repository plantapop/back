from aio_pika import Message
from aio_pika.pool import Pool
from dependency_injector.wiring import Provide, inject

from plantapop.config import Config
from plantapop.shared.domain.event.event_subscriber import EventSubscriber

config = Config.get_instance()


class PikaSubscriber(EventSubscriber):
    exchange_name: str
    binding_key: str

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
            await self._consumming_error(message)

    async def _consumming_error(self, message: Message) -> None:
        if message.headers.get("x-death"):
            if message.headers["x-death"][0]["count"] < config.rabbitmq.max_retries:
                await self.send_to_requeue(message)
            else:
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
        await message.reject(requeue=True)

    async def handle(self, payload: bytes) -> None:
        raise NotImplementedError()
