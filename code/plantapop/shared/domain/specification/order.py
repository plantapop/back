from dataclasses import dataclass


@dataclass
class OrderType:
    ASC = "asc"
    DESC = "desc"


class Order:
    order_type: str

    def __init__(self, field: str):
        self.field = field


class Asc(Order):
    order_type = OrderType.ASC


class Desc(Order):
    order_type = OrderType.DESC
