from uuid import UUID

from pydantic import BaseModel

from plantapop.accounts.domain.exceptions import UserNotFoundException
from plantapop.accounts.domain.user import User
from plantapop.accounts.infrastructure.repository import SQLAlchemyUnitOfWork


class GetUserQuery(BaseModel):
    uuid: UUID


class GetUserQueryResponse(BaseModel):
    uuid: UUID
    username: str
    surname: list[str]
    timezone: str


class GetUserQueryHandler:
    def __init__(self):
        self.uow = SQLAlchemyUnitOfWork()

    async def execute(self, command: GetUserQuery):
        async with self.uow as repo:
            user: User = await repo.get(command.uuid)

            if user is None:
                raise UserNotFoundException

            return GetUserQueryResponse(
                uuid=user.uuid,
                username=user.name,
                surname=user.surnames,
                timezone=user.timezone,
            )
