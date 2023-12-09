from uuid import UUID

from pydantic import BaseModel

from plantapop.accounts.domain.exceptions import UserNotFoundException
from plantapop.accounts.domain.user import User
from plantapop.accounts.infrastructure.repository import SqlUserUnitOfWork


class GetUserQuery(BaseModel):
    uuid: UUID


class GetUserQueryResponse(BaseModel):
    uuid: str
    name: str
    surnames: list[str]
    timezone: str


class GetUserQueryHandler:
    def __init__(self):
        self.uow = SqlUserUnitOfWork()

    async def execute(self, command: GetUserQuery):
        async with self.uow as repo:
            user: User = await repo.get(command.uuid)

            if user is None:
                raise UserNotFoundException

            return GetUserQueryResponse(
                uuid=str(user.uuid),
                name=user.name,
                surnames=user.surnames,
                timezone=user.timezone,
            )
