from test.accounts.domain.user_mother import UserMother

import pytest

from plantapop.accounts.infrastructure.repository import (
    SqlUserUnitOfWork,
    UserDataMapper,
    SQLUser
)


@pytest.fixture
def user(session):
    return UserMother.create()


@pytest.mark.integration
def test_user_data_mapper(user):
    # Given
    mapper = UserDataMapper()

    # When
    model = mapper.entity_to_model(user)
    entity = mapper.model_to_entity(model)

    # Then
    assert isinstance(model, SQLUser)
    assert user == entity
    assert user.__dict__ == entity.__dict__
    assert user.password == entity.password


@pytest.mark.integration
async def test_user_uow(user):
    # Given
    uow = SqlUserUnitOfWork()
    async with uow as repo:
        await repo.save(user)

    # When
    async with uow as repo:
        db_user = await repo.get(user.uuid)

    # Then
    assert isinstance(user.password, bytes)
    assert db_user == user
    assert db_user.__dict__ == user.__dict__
