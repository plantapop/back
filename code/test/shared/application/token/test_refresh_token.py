from test.shared.domain.token.token_mother import TokenMother
from uuid import uuid4

import pytest
from freezegun import freeze_time

from plantapop.config import Config
from plantapop.shared.application.token.refresh_token import RefreshToken
from plantapop.shared.domain.token.exceptions import InvalidTokenException

CONFIGMAP = Config.get_instance()

pytestmark = pytest.mark.shared


@pytest.fixture
async def refresh_token(unit_of_work):
    async with unit_of_work as repo:
        user = {"uuid": uuid4(), "device": "device"}
        valid_refresh = TokenMother.create(
            user_uuid=user["uuid"], device=user["device"]
        )
        user = {"uuid": uuid4(), "device": "device"}
        invalid_refresh = TokenMother.create(
            user_uuid=user["uuid"], device=user["device"], revoked=True
        )
        await repo.save(valid_refresh)
        await repo.save(invalid_refresh)

    rt = RefreshToken()
    rt.uow = unit_of_work
    return {
        "valid": valid_refresh.token,
        "invalid": invalid_refresh.token,
        "uow": unit_of_work,
        "user": user,
        "command": rt,
    }


@pytest.mark.unit
@freeze_time("2021-01-01")
async def test_refresh_token(refresh_token):
    # Given
    token = refresh_token["valid"]
    command = refresh_token["command"]

    # When
    response = await command.execute(token)

    # Then
    assert response["access"]
    assert response["refresh"]
    assert response["refresh"] != token


@pytest.mark.unit
@freeze_time("2021-01-01")
async def test_refresh_token_revoked(refresh_token):
    # Given
    token = refresh_token["invalid"]
    command = refresh_token["command"]

    # When / Then
    with pytest.raises(InvalidTokenException):
        await command.execute(token)


@pytest.mark.unit
@freeze_time("2021-01-01")
async def test_refresh_token_invalid(refresh_token):
    # Given
    command = refresh_token["command"]
    token = "invalid"

    # When / Then
    with pytest.raises(InvalidTokenException):
        await command.execute(token)
