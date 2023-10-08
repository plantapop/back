from pydantic import BaseModel, field_validator


class Email(BaseModel):
    value: str

    @field_validator("value")
    def validate_value(self, v):
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v
