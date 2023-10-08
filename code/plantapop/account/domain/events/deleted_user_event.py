from uuid import UUID


class DeletedUserEvent:
    def __init__(self, user_uuid: UUID):
        self.user_uuid = user_uuid

    def to_dict(self):
        return {"user_id": str(self.user_uuid)}
