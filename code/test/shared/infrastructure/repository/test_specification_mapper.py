from test.shared.infrastructure.repository.conftest import MAP, AlchemyBase

import pytest
from sqlalchemy.orm import Query

from plantapop.shared.domain.specification.filter import (
    Contains,
    Equals,
    LessThan,
    NotEqual,
)
from plantapop.shared.domain.specification.specification import Specification
from plantapop.shared.infrastructure.repository.specification_mapper import (
    SpecificationMapper,
)


@pytest.mark.integration
def test_specification_mapper_case_1(database, john_smith):
    # Given
    spec = Specification(filter=Equals("name", "John") & NotEqual("age", 25))

    # When
    mapper = SpecificationMapper(MAP)
    query: Query = mapper.apply(database.query(AlchemyBase), spec).all()

    # Then
    assert len(query) == 1
    assert query[0].uuid == john_smith.uuid.get()
    assert query[0].table_name == john_smith.name
    assert query[0].table_age == john_smith.age
    assert query[0].table_email == john_smith.email


@pytest.mark.integration
def test_specification_mapper_case_2(database, john_smith, jane_smith):
    # Given
    spec = Specification(
        filter=NotEqual("age", 25) & Equals("name", "John")
        | Contains("email", ["hotmail"])  # noqa
    )

    # When
    mapper = SpecificationMapper(MAP)
    query: Query = mapper.apply(database.query(AlchemyBase), spec).all()

    # Then
    assert len(query) == 2
    assert query[0].uuid == john_smith.uuid.get()
    assert query[0].table_name == john_smith.name
    assert query[0].table_age == john_smith.age
    assert query[0].table_email == john_smith.email
    assert query[1].uuid == jane_smith.uuid.get()
    assert query[1].table_name == jane_smith.name
    assert query[1].table_age == jane_smith.age
    assert query[1].table_email == jane_smith.email


@pytest.mark.integration
def test_specification_mapper_case_3(database):
    # Given

    spec = Specification(
        filter=Equals("name", "John")
        | (NotEqual("age", 25) | (Contains("email", ["hotmail"]) & LessThan("age", 35)))  # noqa
    )

    # When
    mapper = SpecificationMapper(MAP)
    query: Query = mapper.apply(database.query(AlchemyBase), spec).all()

    # Then
    assert len(query) == 4
