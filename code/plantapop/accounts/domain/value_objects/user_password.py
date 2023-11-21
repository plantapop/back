from dataclasses import dataclass

import bcrypt


def validate_password(value: str):
    if not value:
        raise ValueError("Password cannot be empty")


def _crypt_password(value: str) -> tuple[bytes, bytes]:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(value.encode("utf-8"), salt), salt


@dataclass(frozen=True)
class UserPassword:
    value: bytes
    salt: bytes

    @classmethod
    def create(cls, value: str):
        validate_password(value)
        hashed_password, salt = _crypt_password(value)
        return cls(hashed_password, salt)

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def get(self) -> dict[str, bytes]:
        return {"value": self.value, "salt": self.salt}
