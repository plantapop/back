from abc import ABCMeta, abstractmethod
from uuid import UUID

from plantapop.shared.domain.event.domain_event import DomainEvent


class Entity(metaclass=ABCMeta):
    def __eq__(self, other) -> bool:
        if hasattr(other, "uuid"):
            return self.uuid == other.uuid
        return False

    @property
    @abstractmethod
    def uuid(self) -> UUID:
        pass

    def pull_domain_events(self) -> list[DomainEvent]:
        events: list[DomainEvent] = self.events or []
        self.events: list[DomainEvent] = []
        return events


class AggregateRoot(Entity, metaclass=ABCMeta):
    # Each AggregateRoot has a version that is incremented each time it is modified.
    # This is used to detect concurrency conflicts during the commit phase of a UoW.
    # Each AggregateRoot is responsible for incrementing its own version number.
    @property
    @abstractmethod
    def version(self) -> int:
        # return self._version
        pass
