from dataclasses import dataclass

import langcodes


@dataclass(frozen=True)
class UserPreferedLanguages:
    value: list[str]

    def __post_init__(self):
        self._validate_prefered_languages()

    def _validate_prefered_languages(self):
        if not self.value:
            raise ValueError("Prefered languages cannot be empty")

        for language in self.value:
            if len(language) != 2:
                raise ValueError("Invalid language format")
            else:
                if not langcodes.get(language).is_valid():
                    raise ValueError("Invalid language")

    @classmethod
    def create(cls, value: list[str]):
        return cls(value)

    def __eq__(self, other):
        return self.value == other.value

    def get(self):
        return self.value
