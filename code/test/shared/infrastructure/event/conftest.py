import json
from datetime import datetime
from uuid import UUID, uuid4

import pytest

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
            aggregate_uuid=UUID(payload["aggregate_uuid"]),
            event_body=payload["event_body"],
            event_uuid=UUID(payload["event_uuid"]),
            occurred_on=datetime.fromisoformat(payload["occurred_on"]),
        )


class TestEventBus(PikaEventBus):
    exchange_name = "test_exchange"


class FTestEventBus(PikaEventBus):
    exchange_name = "test_exchange"

    async def _publish(self, events: list[DomainEvent]) -> None:
        raise Exception("Error")


class EventBusSubscriber(PikaSubscriber):
    exchange_name = "test_exchange"
    binding_key = "#"

    async def handle(self, payload: bytes) -> None:
        try:
            self._cosas = TestDomainEvent.from_json(payload)
        except Exception:
            self._cosas = None

    async def cosas(self):
        return self._cosas


class FEventBusSubscriber(PikaSubscriber):
    exchange_name = "test_exchange"
    binding_key = "#"

    def __init__(self, retries):
        self._retries = retries
        self.current_retries = 0
        self._cosas = None
        super().__init__()

    async def handle(self, payload: bytes) -> None:
        if self.current_retries < self._retries:
            self.current_retries += 1
            raise Exception("Error")
        else:
            self._cosas = TestDomainEvent.from_json(payload)

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


@pytest.fixture
def failed_event_bus():
    return FTestEventBus()


@pytest.fixture
async def subscriber(event_bus):
    subscriber = EventBusSubscriber()
    await subscriber.subscribe()
    yield subscriber


@pytest.fixture
async def failed_subscriber(failed_event_bus):
    return FEventBusSubscriber
