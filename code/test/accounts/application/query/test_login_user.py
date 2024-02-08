from test.accounts.domain.user_mother import UserMother
from unittest.mock import AsyncMock as Mock

import pytest

from plantapop.accounts.application.query.login_user import (
    LogInUserQuery,
    LogInUserQueryHandler,
    LogInUserResponse,
)

pytestmark = pytest.mark.accounts


@pytest.fixture
def user():
    return UserMother.create(password="password", email="test@test.com")


@pytest.fixture
def token_factory():
    mock = Mock()
    mock.execute.return_value = {"access": "access", "refresh": "refresh"}
    return mock


@pytest.fixture
def query_handler(unit_of_work, token_factory, user):
    lu = LogInUserQueryHandler()
    lu.uow = unit_of_work
    lu.token_factory = token_factory
    lu.uow.repo._db[user.uuid] = user
    return lu


@pytest.fixture
def login_query():
    return LogInUserQuery(device="web", password="password", email="test@test.com")


@pytest.mark.unit
async def test_login_user_returns_tokens(query_handler, login_query):
    # When
    response = await query_handler.execute(login_query)

    # Then
    assert response == LogInUserResponse(refresh_token="refresh", access_token="access")


@pytest.mark.unit
async def test_login_user_returns_none_if_user_not_found(query_handler, login_query):
    # Given
    login_query.email = "fake_email@test.com"

    # When
    response = await query_handler.execute(login_query)

    # Then
    assert response is None


@pytest.mark.unit
async def test_login_user_returns_none_if_password_is_invalid(
    query_handler, login_query
):
    # Given
    login_query.password = "fake_password"

    # When
    response = await query_handler.execute(login_query)

    # Then
    assert response is None


@pytest.mark.unit
async def test_login_user_returns_none_if_user_is_disabled(
    query_handler, login_query, user
):
    # Given
    user.disable()
    query_handler.uow.repo._db[user.uuid] = user

    # When
    response = await query_handler.execute(login_query)

    # Then
    assert response is None
