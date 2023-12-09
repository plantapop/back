from dataclasses import dataclass

from plantapop.shared.domain.specification.filter import Filter
from plantapop.shared.domain.specification.order import Order


@dataclass
class Specification:
    filter: Filter | None = None
    order: Order | None = None
    limit: int | None = None
    offset: int | None = None

    def is_satisfied_by(self, object: object) -> bool:
        return self.filter.is_satisfied_by(object)
