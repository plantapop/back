from datetime import datetime
from uuid import UUID

from plantapop.accounts.domain.events.user_created import UserCreatedEvent
from plantapop.accounts.domain.value_objects import (
    UserEmail,
    UserName,
    UserPassword,
    UserPreferedLanguages,
    UserSurnames,
    UserTimezone,
)
from plantapop.shared.domain.entities import Entity
from plantapop.shared.domain.event.domain_event import DomainEvent
from plantapop.shared.domain.value_objects import GenericUUID


class User(Entity):
    def __init__(
        self,
        uuid: UUID,
        name: str,
        surnames: list[str],
        email: str,
        password: str | bytes,
        timezone: str,
        language: list[str],
        events: list[DomainEvent] | None = [],
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        active: bool = True,
        verified: bool = False,
    ):
        self._uuid = GenericUUID(uuid)
        self._name = UserName(name)
        self._surnames = UserSurnames(surnames)
        self._email = UserEmail(email)
        self._timezone = UserTimezone(timezone)
        self._language = UserPreferedLanguages(language)
        self.events = events
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.active = active
        self.verified = verified

        if isinstance(password, str):  # TODO: Test this
            self._password = UserPassword.create(password)
        elif isinstance(password, bytes):
            self._password = UserPassword(password)
        else:
            raise ValueError("Invalid password type")

    @property
    def uuid(self) -> UUID:
        return self._uuid.get()

    @property
    def name(self) -> str:
        return self._name.get()

    @property
    def surnames(self) -> list[str]:
        return self._surnames.get()

    @property
    def email(self) -> str:
        return self._email.get()

    @property
    def password(self) -> bytes:
        return self._password.get()

    @property
    def timezone(self) -> str:
        return self._timezone.get()

    @property
    def language(self) -> list[str]:
        return self._language.get()

    @classmethod
    def create(
        cls,
        uuid: UUID,
        name: str,
        surnames: list[str],
        email: str,
        password: str,
        timezone: str,
        language: str,
    ):
        return User(
            uuid=uuid,
            name=name,
            surnames=surnames,
            email=email,
            password=password,
            timezone=timezone,
            language=language,
            events=[
                UserCreatedEvent(
                    user_uuid=uuid,
                    user_name=name,
                    surnames=surnames,
                    email=email,
                    prefered_language=language,
                    timezone=timezone,
                )
            ],
        )
