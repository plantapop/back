from uuid import UUID

from plantapop.account.domain.vos.email import Email


class UpdatedPasswordEvent:
    def __init__(self, user_uuid: UUID, email: Email):
        self.user_uuid = user_uuid
        self.email = email

    def to_dict(self):
        return {"user_id": str(self.user_uuid), "email": self.email.value}
