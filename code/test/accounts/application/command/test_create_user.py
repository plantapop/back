from test.accounts.infrastructure.in_memory_event_bus import InMemoryEventBus
from test.accounts.infrastructure.in_memory_repository import InMemoryRepository
from uuid import uuid4

import pytest

from plantapop.accounts.application.command.create_user import CreateUserCommand
from plantapop.accounts.domain.events.user_created import UserCreatedEvent
from plantapop.accounts.domain.exceptions import (
    EmailAlreadyExistsException,
    UserAlreadyExistsException,
)
from plantapop.accounts.infrastructure.dto.registration import RegistrationDto
from plantapop.shared.domain.value_objects import GenericUUID


@pytest.fixture
def database():
    return InMemoryRepository()


@pytest.fixture
def event_bus():
    return InMemoryEventBus()


@pytest.mark.unit
def test_create_user_saves_user(database, event_bus, app_version):
    # Given
    user_uuid = uuid4()
    registration_dto = RegistrationDto(
        app_version=app_version,
        uuid=user_uuid,
        name="test",
        surnames=["test"],
        password="test",
        generate_token=True,
        email="test@test.com",
        prefered_language=["es"],
        timezone="Europe/Madrid",
    )

    # When
    create_user_command = CreateUserCommand(database, event_bus)
    create_user_command.execute(registration_dto)

    # Then
    assert database.save_called is True
    assert database.get(GenericUUID(user_uuid)) is not None


@pytest.mark.unit
def test_create_users_sends_domain_events(database, event_bus, app_version):
    # Given
    user_uuid = uuid4()
    registration_dto = RegistrationDto(
        app_version=app_version,
        uuid=user_uuid,
        name="test",
        surnames=["test"],
        password="test",
        generate_token=True,
        email="test@test.com",
        prefered_language=["es"],
        timezone="Europe/Madrid",
    )

    # When
    create_user_command = CreateUserCommand(database, event_bus)
    create_user_command.execute(registration_dto)

    # Then
    assert event_bus.publish_called is True
    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], UserCreatedEvent)


@pytest.mark.unit
def test_create_user_raises_exception_if_user_already_exists(
    database, event_bus, app_version
):
    # Given
    user_uuid = uuid4()
    registration_dto = RegistrationDto(
        app_version=app_version,
        uuid=user_uuid,
        name="test",
        surnames=["test"],
        password="test",
        generate_token=True,
        email="test@test.com",
        prefered_language=["es"],
        timezone="Europe/Madrid",
    )
    registration_dto_2 = RegistrationDto(
        app_version=app_version,
        uuid=user_uuid,
        name="test2",
        surnames=["test2"],
        password="test2",
        generate_token=False,
        email="test2@test2.com",
        prefered_language=["en"],
        timezone="America/New_York",
    )

    # When
    create_user_command = CreateUserCommand(database, event_bus)
    create_user_command.execute(registration_dto)

    # Then
    with pytest.raises(UserAlreadyExistsException):
        create_user_command.execute(registration_dto_2)

    assert len(event_bus.events) == 1


@pytest.mark.unit
def test_create_user_raises_exception_if_email_already_exists(
    database, event_bus, app_version
):
    # Given
    user_uuid = uuid4()
    registration_dto = RegistrationDto(
        app_version=app_version,
        uuid=user_uuid,
        name="test",
        surnames=["test"],
        password="test",
        generate_token=True,
        email="test@test.com",
        prefered_language=["es"],
        timezone="Europe/Madrid",
    )

    resgistration_dto_2 = RegistrationDto(
        app_version=app_version,
        uuid=uuid4(),
        name="test2",
        surnames=["test2"],
        password="test2",
        generate_token=False,
        email="test@test.com",
        prefered_language=["en"],
        timezone="America/New_York",
    )

    # When
    create_user_command = CreateUserCommand(database, event_bus)
    create_user_command.execute(registration_dto)

    # Then
    with pytest.raises(EmailAlreadyExistsException):
        create_user_command.execute(resgistration_dto_2)

    assert len(event_bus.events) == 1
