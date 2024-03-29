from test.shared.domain.token.token_mother import TokenMother
from uuid import uuid4

import pytest

from plantapop.config import Config
from plantapop.shared.application.token.validate_tokens import ValidateToken

CONFIGMAP = Config.get_instance()

pytestmark = pytest.mark.shared


@pytest.fixture
def validator():
    a_uuid = uuid4()
    b_uuid = uuid4()

    a_r = TokenMother.create(user_uuid=a_uuid, device="a")
    b_r = TokenMother.create(user_uuid=b_uuid, device="b")

    a_a = TokenMother.create(user_uuid=a_uuid, device="a", token_type="access")
    b_a = TokenMother.create(user_uuid=b_uuid, device="b", token_type="access")

    return {
        "a": {
            "uuid": a_uuid,
            "refresh": a_r,
            "access": a_a,
        },
        "b": {
            "uuid": b_uuid,
            "refresh": b_r,
            "access": b_a,
        },
        "command": ValidateToken(),
    }


@pytest.mark.unit
async def test_validate_token(validator):
    # Given
    token = validator["a"]["access"].token

    # When
    uuid = await validator["command"].execute(token)

    # Then
    assert uuid == validator["a"]["uuid"]


@pytest.mark.unit
async def test_validate_refresh_token_invalid(validator):
    # Given
    token = validator["a"]["refresh"].token

    # When
    with pytest.raises(Exception):
        await validator["command"].execute(token)


@pytest.mark.unit
async def test_validate_access_token_invalid(validator):
    # Given
    token = validator["a"]["access"].token + "invalid"

    # When
    with pytest.raises(Exception):
        await validator["command"].execute(token)
