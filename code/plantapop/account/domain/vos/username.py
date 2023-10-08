from pydantic import BaseModel, field_validator


class Username(BaseModel):
    value: str

    @field_validator("value")
    def validate_value(self, v):
        if len(v) < 2:
            raise ValueError("Username must be at least 2 characters long")
        return v
