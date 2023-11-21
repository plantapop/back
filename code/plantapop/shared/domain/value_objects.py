from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID, uuid4

T = TypeVar("T")


@dataclass(frozen=True)
class ValueObject(Generic[T], metaclass=ABCMeta):
    value: T

    def get(self) -> T:
        return self.value

    def __eq__(self, other: "ValueObject") -> bool:
        if hasattr(other, "value"):
            return self.value == other.value
        return False

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)

    def __hash__(self) -> int:
        return hash(self.value)


class GenericUUID(ValueObject[UUID]):
    value = uuid4()
