from shared_kernel.domain.value_objects import GenericUUID


class Entity:
    uuid: GenericUUID

    def __eq__(self, other: "Entity") -> bool:
        if hasattr(other, "uuid"):
            return self.uuid == other.uuid
        return False

    def get_uuid(self) -> GenericUUID:
        return self.uuid
