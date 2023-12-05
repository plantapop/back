from dataclasses import dataclass

import bcrypt
import langcodes
import pytz

from plantapop.config import Config
from plantapop.shared.domain.value_objects import ValueObject

config = Config().get_instance()


@dataclass(frozen=True)
class UserEmail(ValueObject[str]):
    def __post_init__(self):
        self._validate_email()

    def _validate_email(self):
        if not self.value:
            raise ValueError("Email cannot be empty")

        if "@" not in self.value:
            raise ValueError("Email must contain @")


@dataclass(frozen=True)
class UserName(ValueObject[str]):
    def __post_init__(self):
        self._validate_name()

    def _validate_name(self):
        if not self.value:
            raise ValueError("Name cannot be empty")


@dataclass(frozen=True)
class UserPreferedLanguages(ValueObject[list[str]]):
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


def _crypt_password(value: str) -> tuple[bytes, bytes]:
    salt = bcrypt.gensalt(rounds=config.security.password_rounds)
    return bcrypt.hashpw(value.encode("utf-8"), salt)


@dataclass(frozen=True)
class UserPassword(ValueObject[bytes]):
    @classmethod
    def create(cls, value: str):
        if not value:
            raise ValueError("Password cannot be empty")

        hashed_password = _crypt_password(value)
        return cls(hashed_password)

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return bcrypt.checkpw(other.encode("utf-8"), self.value)
        return self.value == other.value


@dataclass(frozen=True)
class UserSurnames(ValueObject[list[str]]):
    def __post_init__(self):
        self._validate_surnames()

    def _validate_surnames(self):
        if not self.value:
            raise ValueError("Surnames cannot be empty")


@dataclass(frozen=True)
class UserTimezone(ValueObject[str]):
    def __post_init__(self):
        self._validate_timezone()

    def _validate_timezone(self):
        if not self.value:
            raise ValueError("Timezone cannot be empty")

        if self.value not in pytz.all_timezones:
            raise ValueError("Invalid timezone")
