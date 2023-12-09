from datetime import datetime as dt
from datetime import timedelta as td
from uuid import uuid4

import pytest
from freezegun import freeze_time
from jose import jwt

from plantapop.config import Config
from plantapop.shared.application.token.create_tokens import CreateToken

CONFIGMAP = Config.get_instance()


@pytest.fixture
def create_token(unit_of_work):
    ct = CreateToken()
    ct.uow = unit_of_work
    return ct


@pytest.fixture
def user():
    return {"uuid": uuid4(), "device": "device"}


@pytest.mark.unit
async def test_create_token(create_token, user):
    # Given
    # When
    tokens = await create_token.execute(user["uuid"], user["device"])

    # Then
    assert isinstance(tokens, dict)
    assert isinstance(tokens["access"], str)
    assert isinstance(tokens["refresh"], str)


@pytest.mark.unit
async def test_create_token_valid_tokens(create_token, user):
    # Given
    tokens = await create_token.execute(user["uuid"], user["device"])

    # When
    access = jwt.decode(
        tokens["access"],
        algorithms=[CONFIGMAP.jwt.algorithm],
        key=CONFIGMAP.jwt.key,
        options={"verify_aud": False},
    )
    refresh = jwt.decode(
        tokens["refresh"],
        algorithms=[CONFIGMAP.jwt.algorithm],
        key=CONFIGMAP.jwt.key,
        options={"verify_aud": False},
    )

    # Then
    assert access["type"] == "access"
    assert refresh["type"] == "refresh"
    assert access["device"] == user["device"]
    assert refresh["device"] == user["device"]
    assert access["uuid"] == str(user["uuid"])
    assert refresh["uuid"] == str(user["uuid"])


@pytest.mark.unit
@freeze_time("2021-01-01 00:00:00")
async def test_create_tokens_uses_configmap_exp_times(create_token, user):
    # Given
    # When
    tokens = await create_token.execute(user["uuid"], user["device"])

    # Then
    access = jwt.decode(
        tokens["access"],
        algorithms=[CONFIGMAP.jwt.algorithm],
        key=CONFIGMAP.jwt.key,
        options={"verify_aud": False},
    )
    refresh = jwt.decode(
        tokens["refresh"],
        algorithms=[CONFIGMAP.jwt.algorithm],
        key=CONFIGMAP.jwt.key,
        options={"verify_aud": False},
    )

    expected_access_exp = (
        dt.utcnow() + td(seconds=CONFIGMAP.jwt.access.duration)
    ).timestamp()
    expected_refresh_exp = (
        dt.utcnow() + td(seconds=CONFIGMAP.jwt.refresh.duration)
    ).timestamp()
    assert access["exp"] == expected_access_exp
    assert refresh["exp"] == expected_refresh_exp


@pytest.mark.unit
async def test_create_token_invalide_old_refresh_token(create_token, user):
    # Given
    await create_token.execute(user["uuid"], user["device"])
    db = create_token.uow.repo._db
    token = list(db.keys())[0]

    # When
    tokens = await create_token.execute(user["uuid"], user["device"])

    # Then
    db = create_token.uow.repo._db
    assert isinstance(tokens, dict)
    assert isinstance(tokens["access"], str)
    assert isinstance(tokens["refresh"], str)
    assert len(db) == 2
    assert db[token].revoked
