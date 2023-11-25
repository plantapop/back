from plantapop.shared.domain.event.event import DomainEvent


class UserCreatedEvent(DomainEvent):
    def __init__(
        self,
        uuid: str,
        name: str,
        surnames: list,
        email: str,
        prefered_language: list,
        timezone: str,
    ):
        self.uuid = uuid
        self.name = name
        self.surnames = surnames
        self.email = email
        self.prefered_language = prefered_language
        self.timezone = timezone

    def to_dict(self) -> dict:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "surnames": self.surnames,
            "email": self.email,
            "prefered_language": self.prefered_language,
            "timezone": self.timezone,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            uuid=data["uuid"],
            name=data["name"],
            surnames=data["surnames"],
            email=data["email"],
            prefered_language=data["prefered_language"],
            timezone=data["timezone"],
        )
