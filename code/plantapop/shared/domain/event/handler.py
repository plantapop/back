from abc import ABCMeta, abstractmethod

from plantapop.shared.domain.event.domain_event import DomainEvent


class Handler(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, event: DomainEvent) -> bool:
        pass
