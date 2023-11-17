from plantapop.accounts.domain.value_objects.user_email import UserEmail
from plantapop.shared.domain.repositories import GenericRepository
from plantapop.shared.domain.value_objects import GenericUUID


class UserRepository(GenericRepository):
    def find_email(self, email: UserEmail):
        raise NotImplementedError

    def find_user(self, uuid: GenericUUID):
        raise NotImplementedError
