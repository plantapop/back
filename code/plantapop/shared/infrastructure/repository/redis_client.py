from redis import asyncio as aioredis

from plantapop.config import Config

config = Config().get_instance()

POOL = aioredis.ConnectionPool.from_url(config.redis.url)


async def get_redis_client() -> aioredis.Redis:
    client = aioredis.Redis.from_pool(POOL)
    return client
