import bcrypt
from pydantic import BaseModel, Field


class Password(BaseModel):
    value: str

    @classmethod
    def create(cls, plain_password: str):
        cls.validate(plain_password)
        hashed_password = bcrypt.hashpw(
            plain_password.encode(), bcrypt.gensalt(rounds=12)
        )
        return cls(value=hashed_password.decode())

    @classmethod
    def validate(cls, plain_password):
        if len(plain_password) < 8:
            raise ValueError("Password must be at least 8 characters long")

    def check_password(self, plain_password: str):
        return bcrypt.checkpw(plain_password.encode(), self.value.encode())
