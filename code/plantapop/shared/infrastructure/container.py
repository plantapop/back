from dependency_injector import containers, providers

from plantapop.shared.infrastructure.controller import endpoints
from plantapop.shared.infrastructure.event import pika_event_bus
from plantapop.shared.infrastructure.event.broker import channel_pool
from plantapop.shared.infrastructure.repository import sqlalchemy_uow
from plantapop.shared.infrastructure.repository.database import session


class SessionContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[sqlalchemy_uow, pika_event_bus, endpoints]
    )

    session = providers.Resource(session)
    channel = providers.Singleton(lambda: channel_pool)
