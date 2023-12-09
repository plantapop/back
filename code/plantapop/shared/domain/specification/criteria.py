from abc import ABCMeta, abstractmethod
from typing import Any


class Criteria(metaclass=ABCMeta):
    description = "No description provided."

    @abstractmethod
    def is_satisfied_by(self, candidate: Any) -> bool:
        pass

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    def __and__(self, crit: "Criteria") -> "_AndCriteria":
        return _AndCriteria(self, crit)

    def __or__(self, crit: "Criteria") -> "_OrCriteria":
        return _OrCriteria(self, crit)

    def __invert__(self) -> "_NotCriteria":
        return _NotCriteria(self)

    def __call__(self, candidate: Any) -> bool:
        return self.is_satisfied_by(candidate)

    def __repr__(self) -> str:
        return f"<{self.class_name}: {self.description}>"


class _AndOrCriteria(Criteria):
    def __init__(self, crit_a: Criteria, crit_b: Criteria) -> None:
        self._crits = (crit_a, crit_b)

    def is_satisfied_by(self, candidate: Any) -> bool:
        results = (crit.is_satisfied_by(candidate) for crit in self._crits)
        return self._check(*results)

    @abstractmethod
    def _check(self, crit_a: bool, crit_b: bool) -> bool:
        pass


class _AndCriteria(_AndOrCriteria):
    def _check(self, crit_a: bool, crit_b: bool) -> bool:
        return crit_a and crit_b


class _OrCriteria(_AndOrCriteria):
    def _check(self, crit_a: bool, crit_b: bool) -> bool:
        return crit_a or crit_b


class _NotCriteria(Criteria):
    def __init__(self, crit: Criteria) -> None:
        self._crit = crit

    def is_satisfied_by(self, candidate: Any) -> bool:
        result = self._crit.is_satisfied_by(candidate)
        return not result
