from test.accounts.domain.user_mother import UserMother
from uuid import uuid4

import pytest

from plantapop.accounts.application.query.get_user import (
    GetUserQuery,
    GetUserQueryHandler,
    GetUserQueryResponse,
)
from plantapop.accounts.domain.exceptions import UserNotFoundException

uuid = uuid4()
password = "test"


@pytest.fixture
def user():
    user = UserMother.create(
        uuid=uuid,
        password=password,
    )
    return user


@pytest.fixture
def query(unit_of_work, user):
    cu = GetUserQueryHandler()
    cu.uow = unit_of_work
    cu.uow.repo._db[user.uuid] = user
    return cu


@pytest.mark.unit
async def test_get_user(query, user):
    # Given
    uuid = user.uuid

    # When
    response = await query.execute(GetUserQuery(uuid=uuid))

    # Then
    assert response == GetUserQueryResponse(
        uuid=str(user.uuid),
        name=user.name,
        surnames=user.surnames,
        timezone=user.timezone,
    )


@pytest.mark.unit
async def test_get_user_not_found(query):
    # Given
    uuid = uuid4()

    # Then
    with pytest.raises(UserNotFoundException):
        # When
        await query.execute(GetUserQuery(uuid=uuid))
