import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

from plantapop.config import Config

config = Config.get_instance()


async def get_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(config.rabbitmq.url)


connection_pool: Pool = Pool(get_connection, max_size=config.rabbitmq.pool_size)


async def get_channel() -> aio_pika.Channel:
    async with connection_pool.acquire() as connection:
        return await connection.channel()


channel_pool: Pool = Pool(get_channel, max_size=config.rabbitmq.channel_pool_size)
