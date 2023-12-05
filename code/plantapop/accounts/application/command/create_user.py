from uuid import UUID

from pydantic import BaseModel

from plantapop.accounts.domain.services import check_email, check_uuid
from plantapop.accounts.domain.user import User
from plantapop.accounts.infrastructure.event_bus import AccountsEventBus
from plantapop.accounts.infrastructure.repository import SqlUserUnitOfWork


class CreateUserCommand(BaseModel):
    app_version: str
    uuid: UUID
    name: str
    surnames: list[str]
    generate_token: bool
    password: str
    email: str
    prefered_language: list[str]
    timezone: str


class CreateUserCommandHandler:
    def __init__(self):
        self.uow = SqlUserUnitOfWork()
        self.event_bus = AccountsEventBus()

    async def execute(self, user_dto: CreateUserCommand):
        user = User.create(
            uuid=user_dto.uuid,
            name=user_dto.name,
            surnames=user_dto.surnames,
            email=user_dto.email,
            password=user_dto.password,
            timezone=user_dto.timezone,
            language=user_dto.prefered_language,
        )
        async with self.uow as repo:
            await check_uuid.check(repository=repo, user=user)
            await check_email.check(repository=repo, user=user)

            await repo.save(user)

        await self.event_bus.publish(user.pull_domain_events())
