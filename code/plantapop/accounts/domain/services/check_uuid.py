from plantapop.accounts.domain.exceptions import UserAlreadyExistsException
from plantapop.accounts.domain.repository import UserRepository
from plantapop.shared.domain.value_objects import GenericUUID


def check(repository: UserRepository, uuid: GenericUUID):
    user = repository.find_user(uuid)
    if user:
        raise UserAlreadyExistsException()
