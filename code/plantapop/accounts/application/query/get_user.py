from uuid import UUID

from pydantic import BaseModel

from plantapop.accounts.domain.user import User
from plantapop.accounts.infrastructure.repository import SQLAlchemyUnitOfWork


class GetUserCommand(BaseModel):
    uuid: UUID


class GetUserCommandResponse(BaseModel):
    uuid: UUID
    username: str
    surname: list[str]
    timezone: str


class GetUserCommandHandler:
    def __init__(self):
        self.unit_of_work = SQLAlchemyUnitOfWork()

    async def execute(self, command: GetUserCommand):
        async with self.unit_of_work as repo:
            user: User = await repo.get(command.uuid)
            return GetUserCommandResponse(
                uuid=user.uuid,
                username=user.name,
                surname=user.surnames,
                timezone=user.timezone,
            )
