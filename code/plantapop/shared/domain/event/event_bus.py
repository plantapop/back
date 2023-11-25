from abc import ABC, abstractmethod

from plantapop.shared.domain.event.event import DomainEvent


class EventBus(ABC):
    @abstractmethod
    def publish(self, events: list[DomainEvent]) -> None:
        pass
