from dataclasses import dataclass

import pytest

from plantapop.shared.domain.specification.filter import (
    Contains,
    Equals,
    GreaterThan,
    LessThan,
    NotContains,
    NotEqual,
)


@dataclass
class Candidate:
    age: int | None = None
    salary: int | None = None
    name: str | None = None


@pytest.mark.unit
def test_equals_filter_satisfied():
    # Given
    candidate = Candidate(age=25)
    equals_filter = Equals(field="age", value=25)

    # When
    result = equals_filter.is_satisfied_by(candidate)

    # Then
    assert result


@pytest.mark.unit
def test_equals_filter_not_satisfied():
    # Given
    candidate = Candidate(age=25)
    equals_filter = Equals(field="age", value=30)

    # When
    result = equals_filter.is_satisfied_by(candidate)

    # Then
    assert not result


@pytest.mark.unit
def test_not_equal_filter_satisfied():
    # Given
    candidate = Candidate(age=25)
    not_equal_filter = NotEqual(field="age", value=30)

    # When
    result = not_equal_filter.is_satisfied_by(candidate)

    # Then
    assert result


@pytest.mark.unit
def test_contains_filter_satisfied():
    # Given
    candidate = Candidate(name="John Doe")
    contains_filter = Contains(field="name", value="John")

    # When
    result = contains_filter.is_satisfied_by(candidate)

    # Then
    assert result


@pytest.mark.unit
def test_not_contains_filter_satisfied():
    # Given
    candidate = Candidate(name="John Doe")
    contains_filter = NotContains(field="name", value="Peter")

    # When
    result = contains_filter.is_satisfied_by(candidate)

    # Then
    assert result


@pytest.mark.unit
def test_and_criteria_satisfied():
    # Given
    candidate = Candidate(age=25, salary=50000)
    age_filter = GreaterThan(field="age", value=20)
    salary_filter = LessThan(field="salary", value=60000)
    and_criteria = age_filter & salary_filter

    # When
    result = and_criteria.is_satisfied_by(candidate)

    # Then
    assert result


@pytest.mark.unit
def test_and_criteria_not_satisfied():
    # Given
    candidate = Candidate(age=25, salary=70000)
    age_filter = GreaterThan(field="age", value=20)
    salary_filter = LessThan(field="salary", value=60000)
    and_criteria = age_filter & salary_filter

    # When
    result = and_criteria.is_satisfied_by(candidate)

    # Then
    assert not result
