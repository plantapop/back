from plantapop.accounts.domain.exceptions import (
    InvalidPasswordException,
    UserNotFoundException,
)
from plantapop.accounts.domain.user import User
from plantapop.shared.domain.repositories import GenericRepository
from plantapop.shared.domain.specification.filter import Equals
from plantapop.shared.domain.specification.specification import Specification


async def check(repository: GenericRepository, email: str, password: str) -> User:
    email_filter = Specification(filter=Equals("email", email), limit=1)

    user: list[User] = await repository.matching(email_filter)
    if len(user) < 1:
        raise UserNotFoundException()

    user = user[0]

    if not user.check_password(password):
        raise InvalidPasswordException()

    return user
