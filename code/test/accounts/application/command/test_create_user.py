from uuid import uuid4

import pytest

from plantapop.accounts.application.command.create_user import CreateUser
from plantapop.accounts.domain.events.user_created import UserCreatedEvent
from plantapop.accounts.domain.exceptions import (
    EmailAlreadyExistsException,
    UserAlreadyExistsException,
)
from plantapop.accounts.infrastructure.dto.registration import RegistrationDto


@pytest.fixture
def create_user_command(unit_of_work, event_bus):
    cu = CreateUser()
    cu.uow = unit_of_work
    cu.event_bus = event_bus
    return cu


@pytest.mark.unit
async def test_create_user_saves_user(create_user_command, app_version):
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
    await create_user_command.execute(registration_dto)

    # Then
    async with create_user_command.uow as repo:
        assert await repo.get(user_uuid) is not None


@pytest.mark.unit
async def test_create_users_sends_domain_events(create_user_command, app_version):
    # Given
    event_bus = create_user_command.event_bus
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
    await create_user_command.execute(registration_dto)

    # Then
    assert event_bus.publish_called is True
    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], UserCreatedEvent)


@pytest.mark.unit
async def test_create_user_raises_exception_if_user_already_exists(
    create_user_command, app_version
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
    await create_user_command.execute(registration_dto)

    # Then
    with pytest.raises(UserAlreadyExistsException):
        await create_user_command.execute(registration_dto_2)

    assert len(create_user_command.event_bus.events) == 1


@pytest.mark.unit
async def test_create_user_raises_exception_if_email_already_exists(
    create_user_command, app_version
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
    await create_user_command.execute(registration_dto)

    # Then
    with pytest.raises(EmailAlreadyExistsException):
        await create_user_command.execute(resgistration_dto_2)

    assert len(create_user_command.event_bus.events) == 1
