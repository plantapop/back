from uuid import UUID

from plantapop.accounts.domain.events.user_created import UserCreatedEvent
from plantapop.accounts.domain.value_objects.user_email import UserEmail
from plantapop.accounts.domain.value_objects.user_name import UserName
from plantapop.accounts.domain.value_objects.user_password import UserPassword
from plantapop.accounts.domain.value_objects.user_prefered_languages import (
    UserPreferedLanguages,
)
from plantapop.accounts.domain.value_objects.user_surnames import UserSurnames
from plantapop.accounts.domain.value_objects.user_timezone import UserTimezone
from plantapop.shared.domain.event.event import DomainEvent
from plantapop.shared.domain.entities import Entity
from plantapop.shared.domain.value_objects import GenericUUID


class User(Entity):
    def __init__(
        self,
        uuid: GenericUUID,
        name: UserName,
        surnames: UserSurnames,
        email: UserEmail,
        password: UserPassword,
        timezone: UserTimezone,
        language: UserPreferedLanguages,
        events: list[DomainEvent] | None = [],
    ):
        self.name = name
        self.surnames = surnames
        self.email = email
        self.password = password
        self.timezone = timezone
        self.language = language
        super().__init__(uuid, events)

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
            uuid=GenericUUID(uuid),
            name=UserName.create(name),
            surnames=UserSurnames.create(surnames),
            email=UserEmail.create(email),
            password=UserPassword.create(password),
            timezone=UserTimezone.create(timezone),
            language=UserPreferedLanguages.create(language),
            events=[
                UserCreatedEvent(
                    uuid=uuid,
                    name=name,
                    surnames=surnames,
                    email=email,
                    prefered_language=language,
                    timezone=timezone,
                )
            ],
        )
