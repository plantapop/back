from dataclasses import dataclass

from plantapop.shared.domain.specification.filter import Criteria
from plantapop.shared.domain.specification.order import Order


@dataclass
class Specification:
    filter: Criteria | None = None
    order: Order | None = None
    limit: int | None = None
    offset: int | None = None

    def is_satisfied_by(self, object: object) -> bool:
        if isinstance(self.filter, Criteria):
            return self.filter.is_satisfied_by(object)
        raise ValueError("Filter must be a Criteria")
