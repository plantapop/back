from test.accounts.domain.user_mother import UserMother
from uuid import uuid4

import pytest

from plantapop.accounts.application.command.update_password import (
    UpdatePasswordCommand,
    UpdatePasswordCommandHandler,
)
from plantapop.accounts.domain.exceptions import (
    InvalidPasswordException,
    UserNotFoundException,
)

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
def command(unit_of_work, user):
    cu = UpdatePasswordCommandHandler()
    cu.uow = unit_of_work
    cu.uow.repo._db[user.uuid] = user
    return cu


@pytest.mark.unit
async def test_update_password(command, user):
    # Given
    user_uuid = user.uuid
    new_password = "new_password"

    # When
    await command.execute(
        UpdatePasswordCommand(
            uuid=user_uuid,
            old_password=password,
            new_password=new_password,
        )
    )

    # Then
    async with command.uow as repo:
        user = await repo.get(user_uuid)
        assert user.check_password(new_password)


@pytest.mark.unit
async def test_update_password_invalid_password_raises_exception(command, user):
    # Given
    user_uuid = user.uuid
    new_password = "new_password"
    old_password = "invalid_password"

    # When
    with pytest.raises(InvalidPasswordException):
        await command.execute(
            UpdatePasswordCommand(
                uuid=user_uuid,
                old_password=old_password,
                new_password=new_password,
            )
        )

    # Then
    async with command.uow as repo:
        user = await repo.get(user_uuid)
        assert user.check_password(password)


@pytest.mark.unit
async def test_update_password_invalid_uuid_raises_exception(command, user):
    # Given
    user_uuid = uuid4()
    new_password = "new_password"

    # When
    with pytest.raises(UserNotFoundException):
        await command.execute(
            UpdatePasswordCommand(
                uuid=user_uuid,
                old_password=password,
                new_password=new_password,
            )
        )

    # Then
    async with command.uow as repo:
        user = await repo.get(user_uuid)
        assert user is None

        user = await repo.get(uuid)
        assert user.check_password(password)
