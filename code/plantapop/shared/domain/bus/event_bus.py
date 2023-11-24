from abc import ABC, abstractmethod

from plantapop.shared.domain.bus.event import DomainEvent


class EventBus(ABC):
    @abstractmethod
    def publish(self, events: list[DomainEvent]) -> None:
        pass
