from plantapop.accounts.domain.exceptions import EmailAlreadyExistsException
from plantapop.accounts.domain.user import User
from plantapop.shared.domain.repositories import GenericRepository
from plantapop.shared.domain.specification.filter import Equals
from plantapop.shared.domain.specification.specification import Specification


async def check(repository: GenericRepository, user: User):
    email_filter = Specification(filter=Equals("email", user.email))
    if await repository.count(email_filter) > 0:
        raise EmailAlreadyExistsException()
