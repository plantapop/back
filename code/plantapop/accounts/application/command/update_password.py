from uuid import UUID

from pydantic import BaseModel

from plantapop.accounts.domain.exceptions import InvalidPasswordException
from plantapop.accounts.domain.user import User
from plantapop.accounts.infrastructure.repository import SQLAlchemyUnitOfWork


class UpdatePasswordCommand(BaseModel):
    uuid: UUID
    old_password: str
    new_password: str


class UpdatePasswordCommandHandler:
    def __init__(self):
        self.uow = SQLAlchemyUnitOfWork()

    async def execute(self, command: UpdatePasswordCommand):
        async with self.uow as repo:
            user: User = await repo.get(command.uuid)
            if not user.check_password(command.old_password):
                raise InvalidPasswordException()
            user.password = command.new_password

            await repo.update(user)
