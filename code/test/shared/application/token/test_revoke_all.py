from test.shared.domain.token.token_mother import TokenMother
from uuid import uuid4

import pytest

from plantapop.config import Config
from plantapop.shared.application.token.revoke_all import RevokeAll
from plantapop.shared.domain.specification.filter import Equals
from plantapop.shared.domain.specification.specification import Specification

CONFIGMAP = Config.get_instance()


@pytest.fixture
async def revoke_all(unit_of_work):
    uuid = uuid4()

    async with unit_of_work as repo:
        await repo.save_all(
            [
                TokenMother.create(user_uuid=uuid, device="a"),
                TokenMother.create(user_uuid=uuid, device="b"),
                TokenMother.create(user_uuid=uuid, device="c"),
                TokenMother.create(user_uuid=uuid, device="d"),
            ]
        )

    rt = RevokeAll()
    rt.uow = unit_of_work
    return {"uuid": uuid, "command": rt, "uow": unit_of_work}


@pytest.mark.unit
async def test_revoke_all(revoke_all):
    # Given
    command = revoke_all["command"]
    uuid = revoke_all["uuid"]

    # When
    await command.execute(uuid)

    # Then
    async with revoke_all["uow"] as repo:
        tokens = await repo.matching(Specification(filter=Equals("user_uuid", uuid)))
        assert all([token.revoked for token in tokens])


@pytest.mark.unit
async def test_revoke_all_no_tokens(revoke_all):
    # Given
    command = revoke_all["command"]
    uuid = uuid4()

    # When
    await command.execute(uuid)

    # Then
    async with revoke_all["uow"] as repo:
        tokens = await repo.matching(Specification(filter=Equals("user_uuid", uuid)))
        assert not tokens
        tokens = await repo.matching(
            Specification(filter=Equals("user_uuid", revoke_all["uuid"]))
        )
        assert all([not token.revoked for token in tokens])
