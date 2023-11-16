from plantapop.accounts.domain.exceptions import (
    EmailAlreadyExistsException,
    UserAlreadyExistsException,
)
from plantapop.accounts.domain.user import User
from plantapop.accounts.domain.value_objects.user_email import UserEmail
from plantapop.shared.domain.value_objects import GenericUUID


class InMemoryRepository:
    def __init__(self):
        self.save_called = False
        self.db = {}

    def save(self, user: User) -> None:
        self.save_called = True
        self.db[user.uuid] = user

    def get(self, uuid: GenericUUID) -> User:
        return self.db[uuid]

    def check_email_is_unique(self, email: UserEmail) -> None:
        for user in self.db.values():
            if user.email == email:
                raise EmailAlreadyExistsException

    def check_user_not_exists(self, uuid: GenericUUID) -> None:
        for user in self.db.values():
            if user.uuid == uuid:
                raise UserAlreadyExistsException
