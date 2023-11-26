from abc import ABC, abstractmethod

# https://chat.openai.com/share/88aa4ca8-b980-4a01-a585-efb95fd605fc


class EventSubscriber(ABC):
    @abstractmethod
    async def subscribed_to(self) -> list:
        pass
