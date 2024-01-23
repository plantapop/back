import json
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID


class DomainEvent(ABC):
    def __init__(
        self,
        event_name: str,
        aggregate_uuid: UUID,
        event_uuid: UUID,
        occurred_on: datetime,
        event_body: dict,
    ):
        self._event_name = event_name
        self._aggregate_uuid = aggregate_uuid
        self._event_uuid = event_uuid
        self._occurred_on = occurred_on
        self._event_body = event_body

    @property
    def event_name(self) -> str:
        return self._event_name

    @property
    def aggregate_uuid(self) -> UUID:
        return self._aggregate_uuid

    @property
    def event_body(self) -> dict:
        return self._event_body

    @property
    def event_uuid(self) -> UUID:
        return self._event_uuid

    @property
    def occurred_on(self) -> datetime:
        return self._occurred_on

    def to_json(self) -> str:
        return json.dumps(
            {
                "event_name": self.event_name,
                "aggregate_uuid": str(self.aggregate_uuid),
                "event_uuid": str(self.event_uuid),
                "occurred_on": self.occurred_on.isoformat(),
                "event_body": self.event_body,
            }
        )

    @classmethod
    @abstractmethod
    def from_json(cls, payload: str) -> "DomainEvent":
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DomainEvent):
            return False

        return (
            self.event_name == other.event_name
            and self.aggregate_uuid == other.aggregate_uuid
            and self.occurred_on == other.occurred_on
        )

    def __str__(self) -> str:
        return f"{self.event_name} - {self.aggregate_uuid} - {self.occurred_on}"

    def __repr__(self) -> str:
        return str(self)
