from sqlalchemy import and_, asc, desc, not_, or_
from sqlalchemy.schema import Column
from sqlalchemy.sql.expression import BinaryExpression, ColumnElement, Select

from plantapop.shared.domain.specification.criteria import (
    Criteria,
    _AndCriteria,
    _AndOrCriteria,
    _NotCriteria,
)
from plantapop.shared.domain.specification.filter import Filter, Operators
from plantapop.shared.domain.specification.order import OrderType
from plantapop.shared.domain.specification.specification import Order, Specification


class SqlAlchemyCriteriaProcessor:
    def __init__(self, map: dict[str, Column]):
        self.map = map

    def to_sqlalchemy_criteria(
        self, criteria: Criteria
    ) -> BinaryExpression | ColumnElement:
        if isinstance(criteria, _AndOrCriteria):
            return self._process_and_or_criteria(criteria)

        elif isinstance(criteria, _NotCriteria):
            return self._process_not_criteria(criteria)

        elif isinstance(criteria, Filter):
            return self._process_filter_criteria(criteria)

        else:
            raise ValueError("Unsupported criteria type")

    def _process_and_or_criteria(self, criteria: _AndOrCriteria) -> ColumnElement:
        crit_a, crit_b = criteria._crits
        operator = and_ if isinstance(criteria, _AndCriteria) else or_

        return operator(
            self.to_sqlalchemy_criteria(crit_a),
            self.to_sqlalchemy_criteria(crit_b),
        )

    def _process_not_criteria(self, criteria: _NotCriteria) -> ColumnElement:
        inner_crit = criteria._crit
        return not_(self.to_sqlalchemy_criteria(inner_crit))

    def _process_filter_criteria(self, criteria: Filter) -> BinaryExpression:
        field = self.map[criteria.field]
        value = criteria.value

        if criteria.operator == Operators.EQUALS:
            return field == value
        elif criteria.operator == Operators.NOT_EQUAL:
            return field != value
        elif criteria.operator == Operators.GT:
            return field > value
        elif criteria.operator == Operators.LT:
            return field < value
        elif criteria.operator == Operators.CONTAINS:
            return field.in_(value)
        elif criteria.operator == Operators.NOT_CONTAINS:
            return ~field.in_(value)
        else:
            raise ValueError("Unsupported filter operator")


class SpecificationMapper:
    def __init__(self, map: dict[str, Column]):
        self.map = map
        self.criteria_processor = SqlAlchemyCriteriaProcessor(self.map)

    def apply(self, query: Select, specification: Specification) -> Select:
        if specification.filter:
            query = query.filter(
                self.criteria_processor.to_sqlalchemy_criteria(specification.filter)
            )

        if specification.order:
            query = query.order_by(self.map_order(specification.order))

        if specification.limit:
            query = query.limit(specification.limit)

        if specification.offset:
            query = query.offset(specification.offset)

        return query

    def map_order(self, order: Order):
        if order.order_type == OrderType.ASC:
            return asc(self.map[order.field])
        elif order.order_type == OrderType.DESC:
            return desc(self.map[order.field])
        else:
            raise ValueError("Unsupported order type")
