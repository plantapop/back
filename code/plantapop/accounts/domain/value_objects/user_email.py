from dataclasses import dataclass


@dataclass(frozen=True)
class UserEmail:
    value: str

    def __post_init__(self):
        self._validate_email()

    def _validate_email(self):
        if not self.value:
            raise ValueError("Email cannot be empty")

        if "@" not in self.value:
            raise ValueError("Email must contain @")

    @classmethod
    def create(cls, value: str):
        return cls(value)

    def __eq__(self, other):
        return self.value == other.value

    def get(self):
        return self.value
