from dataclasses import dataclass
from typing import Any

from plantapop.shared.domain.specification.criteria import Criteria


@dataclass
class Operators:
    EQUALS = "=="
    NOT_EQUAL = "!="
    GT = ">"
    LT = "<"
    CONTAINS = "in"
    NOT_CONTAINS = "not_in"


class Filter(Criteria):
    field: Any
    value: Any

    def __init__(self, field: Any, value: Any):
        self.field = field
        self.value = value


class Equals(Filter):
    operator = Operators.EQUALS

    def is_satisfied_by(self, candidate: Any) -> bool:
        return getattr(candidate, self.field) == self.value


class NotEqual(Filter):
    operator = Operators.NOT_EQUAL

    def is_satisfied_by(self, candidate: Any) -> bool:
        return getattr(candidate, self.field) != self.value


class GreaterThan(Filter):
    operator = Operators.GT

    def is_satisfied_by(self, candidate: Any) -> bool:
        return getattr(candidate, self.field) > self.value


class LessThan(Filter):
    operator = Operators.LT

    def is_satisfied_by(self, candidate: Any) -> bool:
        return getattr(candidate, self.field) < self.value


class Contains(Filter):
    operator = Operators.CONTAINS

    def is_satisfied_by(self, candidate: Any) -> bool:
        return self.value in getattr(candidate, self.field)


class NotContains(Filter):
    operator = Operators.NOT_CONTAINS

    def is_satisfied_by(self, candidate: Any) -> bool:
        return self.value not in getattr(candidate, self.field)
