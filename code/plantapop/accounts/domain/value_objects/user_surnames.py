from dataclasses import dataclass


@dataclass(frozen=True)
class UserSurnames:
    value: list[str]

    def __post_init__(self):
        self._validate_surnames()

    def _validate_surnames(self):
        if not self.value:
            raise ValueError("Surnames cannot be empty")

    @classmethod
    def create(cls, value: list[str]):
        return cls(value)

    def __eq__(self, other):
        return self.value == other.value

    def get(self):
        return self.value
