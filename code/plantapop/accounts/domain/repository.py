from plantapop.accounts.domain.value_objects.user_email import UserEmail
from plantapop.shared.domain.value_objects import GenericUUID
from plantapop.shared.domain.repositories import GenericRepository


class UserRepository(GenericRepository):
    def check_email_is_unique(self, email: UserEmail):
        raise NotImplementedError

    def check_user_not_exists(self, uuid: GenericUUID):
        raise NotImplementedError
