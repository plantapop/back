from dataclasses import dataclass

import pytz


@dataclass(frozen=True)
class UserTimezone:
    value: str

    def __post_init__(self):
        self._validate_timezone()

    def _validate_timezone(self):
        if not self.value:
            raise ValueError("Timezone cannot be empty")

        if self.value not in pytz.all_timezones:
            raise ValueError("Invalid timezone")

    @classmethod
    def create(cls, value: str):
        return cls(value)

    def __eq__(self, other):
        return self.value == other.value

    def get(self):
        return self.value
