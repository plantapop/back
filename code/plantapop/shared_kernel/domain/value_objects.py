from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class GenericUUID:
    value: UUID = uuid4()

    def get(self) -> UUID:
        return self.value

    def __eq__(self, other: "GenericUUID") -> bool:
        if hasattr(other, "value"):
            return self.value == other.value
        return False

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)

    def __hash__(self) -> int:
        return hash(self.value)
