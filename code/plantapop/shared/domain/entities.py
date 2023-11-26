from plantapop.shared.domain.event.domain_event import DomainEvent
from plantapop.shared.domain.value_objects import GenericUUID


class Entity:
    def __init__(self, uuid: GenericUUID, events: list[DomainEvent] = []):
        self.uuid = uuid

    def __eq__(self, other: "Entity") -> bool:
        if hasattr(other, "uuid"):
            return self.uuid == other.uuid
        return False

    def get_uuid(self) -> GenericUUID:
        return self.uuid

    def pull_domain_events(self) -> list[DomainEvent]:
        events = self.events or []
        self.events = []
        return events
