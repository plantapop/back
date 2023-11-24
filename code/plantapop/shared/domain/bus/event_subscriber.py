from abc import ABC, abstractmethod


class EventSubscriber(ABC):
    @abstractmethod
    def subscribed_to(self) -> list:
        pass
