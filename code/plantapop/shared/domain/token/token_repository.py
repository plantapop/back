from abc import ABC, abstractmethod
from uuid import UUID

from plantapop.shared.domain.token.token import Token


class TokenRepository(ABC):
    @abstractmethod
    def get(self, token: str) -> Token:
        pass

    @abstractmethod
    def save(self, token: Token) -> None:
        pass

    @abstractmethod
    def get_token_by_user_and_device(self, uuid: UUID, device: str) -> Token:
        pass

    @abstractmethod
    def find_all_by_user(self, uuid: UUID) -> list[Token]:
        pass

    @abstractmethod
    def save_all(self, tokens: list[Token]) -> None:
        pass
