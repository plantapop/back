import json
from datetime import datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from plantapop.shared.domain.event.domain_event import DomainEvent
from plantapop.shared.infrastructure.event.pika_event_bus import PikaEventBus
from plantapop.shared.infrastructure.event.pika_subscriber import PikaSubscriber


class TestDomainEvent(DomainEvent):
    def __init__(self, aggregate_uuid, event_body, event_uuid, occurred_on):
        self._event_name = (
            "test.plantapop.shared.infrastructure.event.conftest.TestDomainEvent"
        )
        self._aggregate_uuid = aggregate_uuid
        self._event_body = event_body
        self._event_uuid = event_uuid
        self._occurred_on = occurred_on

    @classmethod
    def from_json(cls, payload):
        payload = json.loads(payload)
        return cls(
            aggregate_uuid=payload["aggregate_uuid"],
            event_body=payload["event_body"],
            event_uuid=payload["event_uuid"],
            occurred_on=payload["occurred_on"],
        )


class TestEventBus(PikaEventBus):
    exchange_name = "test_exchange"


class EventBusSubscriber(PikaSubscriber):
    exchange_name = "test_exchange"
    binding_key = "#"

    async def handle(self, event: DomainEvent) -> None:
        self._cosas = 1

    async def cosas(self):
        return self._cosas


@pytest.fixture
def domain_event():
    return TestDomainEvent(
        aggregate_uuid=uuid4(),
        event_body="event_body",
        event_uuid=uuid4(),
        occurred_on=datetime.utcnow(),
    )


@pytest.fixture
def event_bus():
    return TestEventBus()


@pytest_asyncio.fixture
async def subscriber(event_bus):
    subscriber = EventBusSubscriber()
    await subscriber.subscribe()
    yield subscriber
