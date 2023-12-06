from dependency_injector import containers, providers

from plantapop.shared.infrastructure.controller import endpoints
from plantapop.shared.infrastructure.event import (
    pika_event_bus,
    pika_subscriber,
    sqlalchemy_failover_event_bus,
)
from plantapop.shared.infrastructure.event.broker import channel_pool
from plantapop.shared.infrastructure.repository import sqlalchemy_uow
from plantapop.shared.infrastructure.repository.database import session
from plantapop.shared.infrastructure.repository.redis_client import get_redis_client


class SessionContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            sqlalchemy_uow,
            pika_event_bus,
            endpoints,
            sqlalchemy_failover_event_bus,
            pika_subscriber,
        ]
    )

    session = providers.Resource(session)
    channel = providers.Singleton(lambda: channel_pool)
    redis_client = providers.Singleton(lambda: get_redis_client)
