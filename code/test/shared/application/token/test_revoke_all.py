from test.shared.domain.token.token_mother import RefreshTokenMother
from uuid import uuid4

import pytest

from plantapop.config import Config
from plantapop.shared.application.token.revoke_all import RevokeAll
from plantapop.shared.domain.specification.filter import Equals
from plantapop.shared.domain.specification.specification import Specification

CONFIGMAP = Config.get_instance()


@pytest.fixture
def revoke_all(unit_of_work):
    uuid = uuid4()

    with unit_of_work as repo:
        repo.save_all(
            [
                RefreshTokenMother.create(user_uuid=uuid, device="a"),
                RefreshTokenMother.create(user_uuid=uuid, device="b"),
                RefreshTokenMother.create(user_uuid=uuid, device="c"),
                RefreshTokenMother.create(user_uuid=uuid, device="d"),
            ]
        )

    rt = RevokeAll()
    rt.uow = unit_of_work
    return {"uuid": uuid, "command": rt, "uow": unit_of_work}


@pytest.mark.unit
def test_revoke_all(revoke_all):
    # Given
    command = revoke_all["command"]
    uuid = revoke_all["uuid"]

    # When
    command.execute(uuid)

    # Then
    with revoke_all["uow"] as repo:
        tokens = repo.matching(Specification(filter=Equals("user_uuid", uuid)))
        assert all([token.is_revoked() for token in tokens])


@pytest.mark.unit
def test_revoke_all_no_tokens(revoke_all):
    # Given
    command = revoke_all["command"]
    uuid = uuid4()

    # When
    command.execute(uuid)

    # Then
    with revoke_all["uow"] as repo:
        tokens = repo.matching(Specification(filter=Equals("user_uuid", uuid)))
        assert not tokens
        tokens = repo.matching(
            Specification(filter=Equals("user_uuid", revoke_all["uuid"]))
        )
        assert all([not token.is_revoked() for token in tokens])
