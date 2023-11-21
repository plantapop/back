from typing import Optional

from sqlalchemy.orm import Query
from sqlalchemy_filters import apply_filters, apply_sort

from plantapop.shared.domain.specification.criteria import (
    Criteria,
    _AndCriteria,
    _AndOrCriteria,
    _NotCriteria,
)
from plantapop.shared.domain.specification.specification import (
    Filter,
    Order,
    Specification,
)
from plantapop.shared.domain.value_objects import ValueObject


class CriteriaProcessor:
    def __init__(self, map: dict[str, str]):
        self.map = map

    def to_filter_dict(self, criteria: Criteria, parent_operator: str = None) -> dict:
        if isinstance(criteria, _AndOrCriteria):
            return self._process_and_or_criteria(criteria, parent_operator)

        elif isinstance(criteria, _NotCriteria):
            return self._process_not_criteria(criteria)

        elif isinstance(criteria, Filter):
            return self._process_filter_criteria(criteria)

        else:
            raise ValueError("Unsupported criteria type")

    def _process_and_or_criteria(
        self, criteria: Criteria, parent_operator: str
    ) -> dict:
        crit_a, crit_b = criteria._crits
        operator = "and" if isinstance(criteria, _AndCriteria) else "or"

        if parent_operator == operator:
            return self.to_filter_dict(crit_a, operator), self.to_filter_dict(
                crit_b, operator
            )
        else:
            crit_a_filtered = self.to_filter_dict(crit_a, operator)
            crit_b_filtered = self.to_filter_dict(crit_b, operator)
            result = {operator: []}

            if isinstance(crit_a_filtered, dict):
                result[operator].append(crit_a_filtered)
            else:
                result[operator].extend(crit_a_filtered)

            if isinstance(crit_b_filtered, dict):
                result[operator].append(crit_b_filtered)
            else:
                result[operator].extend(crit_b_filtered)

            return result

    def _process_not_criteria(self, criteria: Criteria) -> dict:
        inner_crit = criteria._crit
        return {"not": [inner_crit.to_filter_dict()]}

    def _process_filter_criteria(self, criteria: Criteria) -> dict:
        value = criteria.value

        if isinstance(criteria.value, ValueObject):
            value = criteria.value.get()

        return {
            "field": self.map[
                criteria.field
            ],  # Remember, this is the mapper from Domain Criteria to Infrastructure Criteria # noqa
            "op": criteria.operator,
            "value": value,
        }


class SpecificationMapper:
    def __init__(self, map: dict[str, str]):
        self.map = map

    def apply(self, query: Query, specification: Specification) -> Query:
        if specification.filter:
            filters = self.map_filters(specification.filter)
            query = apply_filters(query, filters)

        if specification.order:
            order = self.map_order(specification.order)
            query = apply_sort(query, order)

        if specification.limit:
            query = query.limit(specification.limit)

        if specification.offset:
            query = query.offset(specification.offset)

        return query

    def map_filters(self, filter: Filter | None) -> list[Optional[Filter]]:
        if filter is None:
            return []
        criteria_processor = CriteriaProcessor(self.map)
        return [criteria_processor.to_filter_dict(filter)]

    def map_order(self, order: Order | None) -> list[Optional[Order]]:
        if order is None:
            return []
        return [{"field": self.map[order.field], "direction": order.order_type}]
