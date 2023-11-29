import json
from datetime import datetime
from uuid import UUID, uuid4

from plantapop.shared.domain.event.domain_event import DomainEvent


class UserCreatedEvent(DomainEvent):
    version: int = 1

    def __init__(
        self,
        user_uuid: UUID,
        user_name: str,
        surnames: list,
        email: str,
        prefered_language: list,
        timezone: str,
        event_uuid: UUID | None = None,
        occurred_on: datetime | None = None,
    ):
        self._event_name = f"plantapop.accounts.{self.version}.event.user.created"
        self._aggregate_uuid = user_uuid
        self._event_uuid = event_uuid or uuid4()
        self._occurred_on = occurred_on or datetime.utcnow()
        self._event_body = {
            "uuid": user_uuid,
            "name": user_name,
            "surnames": surnames,
            "email": email,
            "prefered_language": prefered_language,
            "timezone": timezone,
        }

    @classmethod
    def from_json(cls, json: json) -> "UserCreatedEvent":
        event = json.loads(json)
        return cls(
            user_uuid=UUID(event["aggregate_uuid"]),
            user_name=event["event_body"]["name"],
            surnames=event["event_body"]["surnames"],
            email=event["event_body"]["email"],
            prefered_language=event["event_body"]["prefered_language"],
            timezone=event["event_body"]["timezone"],
            event_uuid=UUID(event["event_uuid"]),
            occurred_on=datetime.fromisoformat(event["occurred_on"]),
        )
