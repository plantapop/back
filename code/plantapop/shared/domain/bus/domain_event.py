from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID


class DomainEvent(ABC):
    @property
    @abstractmethod
    def event_name(self) -> str:
        pass

    @property
    @abstractmethod
    def aggregate_uuid(self) -> UUID:
        pass

    @property
    @abstractmethod
    def event_body(self) -> dict:
        pass

    @property
    @abstractmethod
    def event_uuid(self) -> UUID:
        pass

    @property
    @abstractmethod
    def occurred_on(self) -> datetime:
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DomainEvent):
            return False

        return (
            self.event_name == other.event_name
            and self.aggregate_id == other.aggregate_id
            and self.occurred_on == other.occurred_on
        )

    def __str__(self) -> str:
        return f"{self.event_name} - {self.aggregate_id} - {self.occurred_on}"

    def __repr__(self) -> str:
        return str(self)
