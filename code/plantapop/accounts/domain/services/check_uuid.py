from plantapop.accounts.domain.exceptions import UserAlreadyExistsException
from plantapop.accounts.domain.user import User
from plantapop.shared.domain.repositories import GenericRepository


async def check(repository: GenericRepository, user: User):
    if await repository.exists(user.uuid):
        raise UserAlreadyExistsException()
