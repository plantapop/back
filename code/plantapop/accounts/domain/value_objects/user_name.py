from dataclasses import dataclass


@dataclass(frozen=True)
class UserName:
    value: str

    def __post_init__(self):
        self._validate_name()

    def _validate_name(self):
        if not self.value:
            raise ValueError("Name cannot be empty")

    @classmethod
    def create(cls, value: str):
        return cls(value)

    def __eq__(self, other):
        return self.value == other.value

    def get(self):
        return self.value
