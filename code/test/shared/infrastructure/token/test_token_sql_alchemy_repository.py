from test.shared.domain.token.token_mother import TokenMother

import pytest

from plantapop.shared.domain.specification.filter import Equals
from plantapop.shared.domain.specification.specification import Specification
from plantapop.shared.infrastructure.token.token_repository import (
    RefreshToken,
    RefreshTokenUoW,
    TokenDataMapper,
)


@pytest.fixture
def refresh_token(isolated):
    return TokenMother.create()


@pytest.mark.integration
def test_refresh_token_model_to_entity(refresh_token):
    # Given
    mapper = TokenDataMapper()
    valid_model = RefreshToken(
        uuid=refresh_token.uuid.get(),
        token=refresh_token.token,
        user_uuid=refresh_token.user_uuid.get(),
        device=refresh_token.device,
        expiration_date=refresh_token.exp,
        revoked=refresh_token.revoked,
    )

    # When
    entity = mapper.model_to_entity(valid_model)

    # Then
    assert entity.uuid == refresh_token.uuid
    assert entity.token == refresh_token.token
    assert entity.user_uuid == refresh_token.user_uuid
    assert entity.device == refresh_token.device
    assert entity.exp == refresh_token.exp
    assert entity.revoked == refresh_token.revoked


@pytest.mark.integration
def test_refresh_token_entity_to_model(refresh_token):
    # Given
    mapper = TokenDataMapper()

    # When
    model = mapper.entity_to_model(refresh_token)

    # Then
    assert model.uuid == refresh_token.uuid.get()
    assert model.token == refresh_token.token
    assert model.user_uuid == refresh_token.user_uuid.get()
    assert model.device == refresh_token.device
    assert model.expiration_date == refresh_token.exp
    assert model.revoked == refresh_token.revoked


@pytest.mark.integration
def test_refresh_token_uow(refresh_token):
    # Given
    uow = RefreshTokenUoW()
    with uow as repo:
        repo.save(refresh_token)

    # When
    with uow as repo:
        token = repo.get(refresh_token.uuid)

    # Then
    assert token.uuid == refresh_token.uuid
    assert token.token == refresh_token.token
    assert token.user_uuid == refresh_token.user_uuid
    assert token.device == refresh_token.device
    assert token.exp == refresh_token.exp


@pytest.mark.integration
def test_refresh_token_uow_get_by_token(refresh_token):
    # Given
    uow = RefreshTokenUoW()
    specification = Specification(filter=Equals("token", refresh_token.token))

    with uow as repo:
        repo.save(refresh_token)

    # When
    with uow as repo:
        token_list = repo.matching(specification)

    # Then
    assert len(token_list) == 1
    token = token_list[0]
    assert token.uuid == refresh_token.uuid
    assert token.token == refresh_token.token
    assert token.user_uuid == refresh_token.user_uuid
    assert token.device == refresh_token.device
    assert token.exp == refresh_token.exp
