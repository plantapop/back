from plantapop.shared.domain.bus.event import DomainEvent
from plantapop.shared.domain.bus.event_bus import EventBus


class InMemoryEventBus(EventBus):
    def __init__(self):
        self.events = []
        self.publish_called = False

    def publish(self, events: list[DomainEvent]) -> None:
        self.events.extend(events)
        self.publish_called = True
