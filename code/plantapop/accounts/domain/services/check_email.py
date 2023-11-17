from plantapop.accounts.domain.exceptions import EmailAlreadyExistsException
from plantapop.accounts.domain.repository import UserRepository
from plantapop.accounts.domain.value_objects.user_email import UserEmail


def check(repository: UserRepository, email: UserEmail):
    user = repository.find_email(email)
    if user:
        raise EmailAlreadyExistsException()
