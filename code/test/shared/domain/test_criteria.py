import pytest

from plantapop.shared.domain.specification.criteria import Criteria


class MockEntity:
    pass


class MockSpecification(Criteria):
    def is_satisfied_by(self, candidate):
        return True


class MockFalseSpecification(Criteria):
    def is_satisfied_by(self, candidate):
        return False


@pytest.mark.unit
def test_and_specification():
    spec1 = MockSpecification()
    spec2 = MockSpecification()
    and_spec = spec1 & spec2

    assert and_spec.is_satisfied_by(MockEntity()) is True


@pytest.mark.unit
def test_or_specification():
    spec1 = MockFalseSpecification()
    spec2 = MockFalseSpecification()
    or_spec = spec1 | spec2

    assert or_spec.is_satisfied_by(MockEntity()) is False


@pytest.mark.unit
def test_not_specification():
    spec = MockFalseSpecification()
    not_spec = ~spec

    assert not_spec.is_satisfied_by(MockEntity()) is True


@pytest.mark.unit
def test_complex_specification():
    spec1 = MockSpecification()
    spec2 = MockFalseSpecification()
    spec3 = MockFalseSpecification()

    complex_spec = spec1 & (spec2 | ~spec3)

    assert complex_spec.is_satisfied_by(MockEntity()) is True
