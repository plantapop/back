import copy
from test.shared.infrastructure.repository.conftest import (
    MAP,
    AlchemyBase,
    TestBaseDataMapper,
)
from uuid import uuid4

import pytest

from plantapop.shared.domain.specification.filter import Equals
from plantapop.shared.domain.specification.specification import Specification
from plantapop.shared.domain.value_objects import GenericUUID
from plantapop.shared.infrastructure.repository.specification_mapper import (
    SpecificationMapper,
)
from plantapop.shared.infrastructure.repository.sqlalchemy_repository import (
    SQLAlchemyRepository,
)
from plantapop.shared.infrastructure.repository.sqlalchemy_uow import (
    SQLAlchemyUnitOfWork,
)


class AlchTestRep(SQLAlchemyRepository):
    specification_mapper = SpecificationMapper(MAP)
    mapper = TestBaseDataMapper()
    model = AlchemyBase


class SqlTestUoW(SQLAlchemyUnitOfWork):
    repo = AlchTestRep


@pytest.fixture
def repository(isolated):
    with SqlTestUoW() as repo:
        yield repo


@pytest.mark.integration
def test_get_repository(repository, john_smith):
    # Given
    uuid = john_smith.uuid

    # When
    entity = repository.get(uuid)

    # Then
    assert entity.uuid == john_smith.uuid


@pytest.mark.integration
def test_get_random_repository(repository):
    # Given
    uuid = GenericUUID(uuid4())

    # When
    entity = repository.get(uuid)

    # Then
    assert entity is None


@pytest.mark.integration
def test_count_repository(repository, john_smith, jane_smith):
    # Given
    spec = Specification(filter=Equals("name", "John") | Equals("name", "Jane"))

    # When
    count = repository.count(spec)

    # Then
    assert count == 4


@pytest.mark.integration
def test_count_repository_no_spec(repository):
    # Given

    # When
    count = repository.count()

    # Then
    assert count == 4


@pytest.mark.integration
def test_save_repository(repository, john_smith):
    # Given
    new_persn = copy.deepcopy(john_smith)
    new_persn.uuid = GenericUUID(uuid4())
    new_persn.name = "John Smith"
    total = repository.count()

    # When
    repository.save(new_persn)
    repository.commit()

    # Then
    assert repository.get(new_persn.uuid).name == "John Smith"
    assert repository.count() == total + 1


@pytest.mark.integration
def test_save_all_repository(repository, john_smith, jane_smith):
    # Given
    new_john_smith = copy.deepcopy(john_smith)
    new_john_smith.uuid = GenericUUID(uuid4())
    new_john_smith.name = "John Smith"

    new_jane_smith = copy.deepcopy(jane_smith)
    new_jane_smith.uuid = GenericUUID(uuid4())
    new_jane_smith.name = "Jane Smith"

    total = repository.count()

    # When
    repository.save_all([new_john_smith, new_jane_smith])
    repository.commit()

    # Then
    assert repository.get(new_john_smith.uuid).name == "John Smith"
    assert repository.get(new_jane_smith.uuid).name == "Jane Smith"
    assert repository.count() == total + 2


@pytest.mark.integration
def test_update_repository(repository, john_smith):
    # Given
    john_smith.name = "John Smith"
    total = repository.count()

    # When
    repository.update(john_smith)
    repository.commit()

    # Then
    assert repository.get(john_smith.uuid).name == "John Smith"
    assert repository.count() == total


@pytest.mark.integration
def test_update_all_repository(repository, john_smith, jane_smith):
    # Given
    john_smith.name = "John Smith"
    jane_smith.name = "Jane Smith"
    total = repository.count()

    # When
    repository.update_all([john_smith, jane_smith])
    repository.commit()

    # Then
    assert repository.get(john_smith.uuid).name == "John Smith"
    assert repository.get(jane_smith.uuid).name == "Jane Smith"
    assert repository.count() == total


@pytest.mark.integration
def test_delete_repository(repository, john_smith):
    # Given
    total = repository.count()

    # When
    repository.delete(john_smith)
    repository.commit()

    # Then
    assert repository.get(john_smith.uuid) is None
    assert repository.count() == total - 1


@pytest.mark.integration
def test_delete_all_repository(repository, john_smith, jane_smith):
    # Given
    total = repository.count()

    # When
    repository.delete_all([john_smith, jane_smith])
    repository.commit()

    # Then
    assert repository.get(john_smith.uuid) is None
    assert repository.get(jane_smith.uuid) is None
    assert repository.count() == total - 2


@pytest.mark.integration
def test_exists_repository(repository, john_smith):
    # Given

    # When
    exists = repository.exists(john_smith.uuid)

    # Then
    assert exists is True


@pytest.mark.integration
def test_exists_repository_no_spec(repository):
    # Given

    # When
    exists = repository.exists(GenericUUID(uuid4()))

    # Then
    assert exists is False


@pytest.mark.integration
def test_exists_repository_spec(repository, john_smith):
    # Given
    spec = Specification(filter=Equals("name", "John"))

    # When
    exists = repository.exists(spec=spec)

    # Then
    assert exists is True


@pytest.mark.integration
def test_exists_repository_spec_no_match(repository, john_smith):
    # Given
    spec = Specification(filter=Equals("name", "Juan"))

    # When
    exists = repository.exists(spec=spec)

    # Then
    assert exists is False


@pytest.mark.integration
def test_matching(repository, jane_smith):
    # Given
    spec = Specification(filter=Equals("name", "Jane") & Equals("age", 35))

    # When
    entities = repository.matching(spec)

    # Then
    assert len(entities) == 1
    assert entities[0].name == "Jane"


@pytest.mark.integration
def test_matching_no_spec(repository):
    # Given

    # When
    entities = repository.matching(Specification())

    # Then
    assert len(entities) == 4


@pytest.mark.integration
def test_matching_no_match(repository):
    # Given
    spec = Specification(filter=Equals("name", "Juan"))

    # When
    entities = repository.matching(spec)

    # Then
    assert len(entities) == 0


@pytest.mark.integration
def test_matching_no_match_spec(repository):
    # Given
    spec = Specification(filter=Equals("name", "Juan") & Equals("age", 35))

    # When
    entities = repository.matching(spec)

    # Then
    assert len(entities) == 0
