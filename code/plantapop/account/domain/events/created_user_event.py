from uuid import UUID

from plantapop.account.domain.vos.email import Email
from plantapop.account.domain.vos.username import Username


class CreatedUserEvent:
    def __init__(self, user_uuid: UUID, email: Email, username: Username):
        self.user_uuid = user_uuid
        self.email = email
        self.username = username

    def to_dict(self):
        return {
            "user_id": str(self.user_uuid),
            "email": self.email.value,
            "username": self.username.value,
        }
