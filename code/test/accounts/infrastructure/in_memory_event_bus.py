from plantapop.shared.domain.event.event import DomainEvent
from plantapop.shared.domain.event.event_bus import EventBus


class InMemoryEventBus(EventBus):
    def __init__(self):
        self.events = []
        self.publish_called = False

    def publish(self, events: list[DomainEvent]) -> None:
        self.events.extend(events)
        self.publish_called = True
