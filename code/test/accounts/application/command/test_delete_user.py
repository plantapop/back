from test.accounts.domain.user_mother import UserMother
from uuid import uuid4

import pytest

from plantapop.accounts.application.command.delete_user import (
    DeleteUserCommand,
    DeleteUserCommandHandler,
)
from plantapop.accounts.domain.events.user_deleted import UserDeletedEvent
from plantapop.accounts.domain.exceptions import InvalidPasswordException

uuid = uuid4()
password = "test"


pytestmark = pytest.mark.accounts


@pytest.fixture
def user():
    user = UserMother.create(
        uuid=uuid,
        password=password,
    )
    return user


@pytest.fixture
def command(unit_of_work, event_bus, user):
    cu = DeleteUserCommandHandler()
    cu.uow = unit_of_work
    cu.event_bus = event_bus
    cu.uow.repo._db[user.uuid] = user
    return cu


@pytest.mark.unit
async def test_delete_user(command, user):
    # Given
    user_uuid = user.uuid

    # When
    await command.execute(
        DeleteUserCommand(
            uuid=user_uuid,
            password=password,
        )
    )

    # Then
    async with command.uow as repo:
        assert await repo.get(user_uuid) is None


@pytest.mark.unit
async def test_delete_user_invalid_password_raises_exception(command, user):
    # Given
    user_uuid = user.uuid
    password = "invalid_password"

    # When
    with pytest.raises(InvalidPasswordException):
        await command.execute(
            DeleteUserCommand(
                uuid=user_uuid,
                password=password,
            )
        )

    # Then
    async with command.uow as repo:
        assert await repo.get(user_uuid) is not None


@pytest.mark.unit
async def test_delete_user_creates_domain_event(command, user):
    # Given
    user_uuid = user.uuid

    # When
    await command.execute(
        DeleteUserCommand(
            uuid=user_uuid,
            password=password,
        )
    )

    # Then
    assert len(command.event_bus.events) == 1
    assert command.event_bus.events[0].__class__ == UserDeletedEvent
    assert command.event_bus.events[0].event_body["uuid"] == str(user_uuid)
    assert command.event_bus.events[0].event_body["name"] == user.name
