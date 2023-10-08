from abc import ABC, abstractmethod
from uuid import UUID

from plantapop.account.domain.entities.user import User


class Repository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, user_uuid: UUID) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user: User) -> None:
        raise NotImplementedError
