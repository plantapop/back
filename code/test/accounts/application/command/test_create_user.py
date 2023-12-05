from uuid import uuid4

import pytest
from pydantic import ValidationError

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


@pytest.fixture
def registration_dto(app_version):
    return RegistrationDto(
        app_version=app_version,
        uuid=uuid4(),
        name="test",
        surnames=["test"],
        password="test",
        generate_token=True,
        email="test@test.com",
        prefered_language=["es"],
        timezone="Europe/Madrid",
    )


@pytest.mark.unit
async def test_create_user_saves_user(create_user_command, registration_dto):
    # Given
    user_uuid = registration_dto.uuid

    # When
    await create_user_command.execute(registration_dto)

    # Then
    async with create_user_command.uow as repo:
        assert await repo.get(user_uuid) is not None


@pytest.mark.unit
async def test_create_users_sends_domain_events(create_user_command, registration_dto):
    # Given
    event_bus = create_user_command.event_bus

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
    async with create_user_command.uow as repo:
        user = await repo.get(user_uuid)
        assert user.name == "test"
        assert user.email == "test@test.com"


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

    uuid_user_2 = uuid4()

    resgistration_dto_2 = RegistrationDto(
        app_version=app_version,
        uuid=uuid_user_2,
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
    async with create_user_command.uow as repo:
        assert await repo.get(uuid_user_2) is None


@pytest.mark.unit
async def test_create_user_invalid_email_raises_exception(
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
        email="invalid_email",
        prefered_language=["es"],
        timezone="Europe/Madrid",
    )

    # When
    with pytest.raises(ValueError):
        await create_user_command.execute(registration_dto)

    # Then
    assert len(create_user_command.event_bus.events) == 0
    async with create_user_command.uow as repo:
        assert await repo.get(user_uuid) is None


@pytest.mark.unit
async def test_create_user_invalid_prefered_language_raises_exception(
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
        prefered_language=["invalid_language"],
        timezone="Europe/Madrid",
    )

    # When
    with pytest.raises(ValueError):
        await create_user_command.execute(registration_dto)

    # Then
    assert len(create_user_command.event_bus.events) == 0
    async with create_user_command.uow as repo:
        assert await repo.get(user_uuid) is None


@pytest.mark.unit
async def test_create_user_invalid_timezone_raises_exception(
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
        timezone="invalid_timezone",
    )

    # When
    with pytest.raises(ValueError):
        await create_user_command.execute(registration_dto)

    # Then
    assert len(create_user_command.event_bus.events) == 0
    async with create_user_command.uow as repo:
        assert await repo.get(user_uuid) is None


@pytest.mark.unit
async def test_create_user_invalid_password_raises_exception(
    create_user_command, app_version
):
    # Given
    user_uuid = uuid4()
    registration_dto = RegistrationDto(
        app_version=app_version,
        uuid=user_uuid,
        name="test",
        surnames=["test"],
        password="",
        generate_token=True,
        email="test@test.com",
        prefered_language=["es"],
        timezone="Europe/Madrid",
    )

    # When
    with pytest.raises(ValueError):
        await create_user_command.execute(registration_dto)

    # Then
    assert len(create_user_command.event_bus.events) == 0
    async with create_user_command.uow as repo:
        assert await repo.get(user_uuid) is None


@pytest.mark.unit
async def test_create_user_invalid_name_raises_exception(
    create_user_command, app_version
):
    # Given
    user_uuid = uuid4()
    registration_dto = RegistrationDto(
        app_version=app_version,
        uuid=user_uuid,
        name="",
        surnames=["test"],
        password="test",
        generate_token=True,
        email="test@test.com",
        prefered_language=["es"],
        timezone="Europe/Madrid",
    )

    # When
    with pytest.raises(ValueError):
        await create_user_command.execute(registration_dto)

    # Then
    assert len(create_user_command.event_bus.events) == 0
    async with create_user_command.uow as repo:
        assert await repo.get(user_uuid) is None


@pytest.mark.unit
async def test_create_user_invalid_surnames_raises_exception(
    create_user_command, app_version
):
    # Given
    user_uuid = uuid4()
    registration_dto = RegistrationDto(
        app_version=app_version,
        uuid=user_uuid,
        name="test",
        surnames=[],
        password="test",
        generate_token=True,
        email="test@test.com",
        prefered_language=["es"],
        timezone="Europe/Madrid",
    )

    # When
    with pytest.raises(ValueError):
        await create_user_command.execute(registration_dto)

    # Then
    assert len(create_user_command.event_bus.events) == 0
    async with create_user_command.uow as repo:
        assert await repo.get(user_uuid) is None


@pytest.mark.unit
async def test_create_user_invalid_uuid_raises_exception(
    create_user_command, app_version
):
    # Given
    with pytest.raises(ValidationError):
        RegistrationDto(
            app_version=app_version,
            uuid="invalid_uuid",
            name="test",
            surnames=["test"],
            password="test",
            generate_token=True,
            email="test@test.com",
            prefered_language=["es"],
            timezone="Europe/Madrid",
        )
