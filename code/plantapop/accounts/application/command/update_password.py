from uuid import UUID

from pydantic import BaseModel

from plantapop.accounts.domain.exceptions import (
    InvalidPasswordException,
    UserNotFoundException,
)
from plantapop.accounts.domain.user import User
from plantapop.accounts.infrastructure.repository import SqlUserUnitOfWork


class UpdatePasswordCommand(BaseModel):
    uuid: UUID
    old_password: str
    new_password: str


class UpdatePasswordCommandHandler:
    def __init__(self):
        self.uow = SqlUserUnitOfWork()

    async def execute(self, command: UpdatePasswordCommand):
        async with self.uow as repo:
            user: User | None = await repo.get(command.uuid)
            if user is None:
                raise UserNotFoundException()
            if not user.check_password(command.old_password):
                raise InvalidPasswordException()
            user.password = command.new_password  # type: ignore

            await repo.update(user)
