from abc import ABC, abstractmethod

from plantapop.shared.domain.event.domain_event import DomainEvent


class EventBus(ABC):
    @abstractmethod
    async def publish(self, events: list[DomainEvent]) -> None:
        pass
