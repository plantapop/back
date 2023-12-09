from uuid import UUID

from pydantic import BaseModel

from plantapop.accounts.infrastructure.event_bus import AccountsEventBus
from plantapop.accounts.infrastructure.repository import SqlUserUnitOfWork


class DeleteUserCommand(BaseModel):
    uuid: UUID
    password: str


class DeleteUserCommandHandler:
    def __init__(self):
        self.uow = SqlUserUnitOfWork()
        self.event_bus = AccountsEventBus()

    async def execute(self, user_dto: DeleteUserCommand):
        async with self.uow as repo:
            user = await repo.get(user_dto.uuid)
            user.delete(user_dto.password)
            await repo.delete(user)
        await self.event_bus.publish(user.pull_domain_events())
