from pydantic import BaseModel

from plantapop.accounts.domain.exceptions import (
    InvalidPasswordException,
    UserNotFoundException,
)
from plantapop.accounts.domain.services import check_exists
from plantapop.accounts.infrastructure.repository import SqlUserUnitOfWork
from plantapop.shared.application.token.create_tokens import CreateToken


class LogInUserQuery(BaseModel):
    platform: str
    password: str
    email: str


class LogInUserResponse(BaseModel):
    refresh_token: str
    access_token: str


class LoginUserQueryHandler:
    def __init__(self):
        self.uow = SqlUserUnitOfWork()
        self.token_factory = CreateToken()

    async def execute(self, dto: LogInUserQuery) -> LogInUserResponse | None:
        try:
            async with self.uow as repo:
                user = await check_exists.check(
                    repository=repo, email=dto.email, password=dto.password
                )
        except (UserNotFoundException, InvalidPasswordException):
            return None

        tokens = await self.token_factory.execute(user.uuid, dto.platform)

        return LogInUserResponse(
            refresh_token=tokens["refresh"], access_token=tokens["access"]
        )
