from datetime import datetime
from uuid import UUID, uuid4

from plantapop.accounts.domain.user import User
from plantapop.shared.domain.event.domain_event import DomainEvent


class UserMother:
    @staticmethod
    def create(
        uuid: UUID = uuid4(),
        name: str = "TestUser",
        surnames: list[str] = ["TestSurname"],
        email: str = "test@test.com",
        password: str | bytes = "test_password",
        timezone: str = "Europe/Madrid",
        language: list[str] = ["en"],
        events: list[DomainEvent] | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        active: bool = True,
        verified: bool = False,
    ):
        return User(
            uuid=uuid,
            name=name,
            surnames=surnames,
            email=email,
            password=password,
            timezone=timezone,
            language=language,
            events=events or [],
            created_at=created_at,
            updated_at=updated_at,
            active=active,
            verified=verified,
        )
