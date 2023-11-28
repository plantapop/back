from test.shared.infrastructure.repository.conftest import MAP, AlchemyBase

import pytest
from sqlalchemy import select

from plantapop.shared.domain.specification.filter import (
    Contains,
    Equals,
    GreaterThan,
    LessThan,
    NotContains,
    NotEqual,
)
from plantapop.shared.domain.specification.order import Desc
from plantapop.shared.domain.specification.specification import Specification
from plantapop.shared.infrastructure.repository.specification_mapper import (
    SpecificationMapper,
)


@pytest.mark.integration
async def test_specification_mapper_case_1(asession, john_smith):
    # Given
    spec = Specification(filter=Equals("name", "John") & NotEqual("age", 25))

    # When
    raw = await asession.execute(
        SpecificationMapper(MAP).apply(select(AlchemyBase), spec)
    )
    query = raw.scalars().all()

    # Then
    assert len(query) == 1
    assert query[0].uuid == john_smith.uuid.get()
    assert query[0].table_name == john_smith.name
    assert query[0].table_age == john_smith.age
    assert query[0].table_email == john_smith.email


@pytest.mark.integration
async def test_specification_mapper_case_2(asession, john_smith, jane_smith):
    # Given
    spec = Specification(
        filter=NotEqual("age", 25) & Equals("name", "John")
        | Contains("email", ["hotmail"])  # noqa
    )

    # When
    raw = await asession.execute(
        SpecificationMapper(MAP).apply(select(AlchemyBase), spec)
    )
    query = raw.scalars().all()

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
async def test_specification_mapper_case_3(asession):
    # Given

    spec = Specification(
        filter=Equals("name", "John")
        | (
            NotEqual("age", 25) | (Contains("email", ["hotmail"]) & LessThan("age", 35))
        )  # noqa
    )

    # When
    raw = await asession.execute(
        SpecificationMapper(MAP).apply(select(AlchemyBase), spec)
    )
    query = raw.scalars().all()

    # Then
    assert len(query) == 4


@pytest.mark.integration
async def test_specification_mapper_case_4(asession, jane_smith):
    # Given
    spec = Specification(
        filter=NotContains("email", ["gmail"]) & GreaterThan("age", 20),
        order=Desc("age"),
        limit=1,
    )

    # When
    raw = await asession.execute(
        SpecificationMapper(MAP).apply(select(AlchemyBase), spec)
    )
    query = raw.scalars().all()

    # Then
    assert len(query) == 1
    assert query[0].table_age == jane_smith.age
    assert query[0].table_name == jane_smith.name


@pytest.mark.integration
async def test_specification_mapper_case_5(asession, john_smith):
    # Given
    spec = Specification(
        filter=NotContains("email", ["gmail"]) & GreaterThan("age", 20),
        order=Desc("age"),
        limit=1,
        offset=1,
    )

    # When
    raw = await asession.execute(
        SpecificationMapper(MAP).apply(select(AlchemyBase), spec)
    )
    query = raw.scalars().all()

    # Then
    assert len(query) == 1
    assert query[0].table_age == john_smith.age
    assert query[0].table_name == john_smith.name
