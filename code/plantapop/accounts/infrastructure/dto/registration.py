from uuid import UUID

from pydantic import BaseModel


class RegistrationDto(BaseModel):
    app_version: str
    uuid: UUID
    name: str
    surnames: list[str]
    generate_token: bool
    password: str
    email: str
    prefered_language: list[str]
    timezone: str
