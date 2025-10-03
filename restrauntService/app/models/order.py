from app.models.order_item import OrderItem
from app.observers.order_observer import OrderSubject
from uuid import uuid4
from app.models.customer import Customer


class Order(OrderSubject):
    def __init__(self, table_number: int, items: list[OrderItem], ordered_by: Customer) -> None:
        super().__init__()
        self.order_id = str(uuid4())
        self.table_number = table_number
        self.items: list[OrderItem] = items
        self.ordered_by = ordered_by
        self.add_observer(ordered_by)

    def get_order_id(self) -> str:
        return self.order_id

    def get_table_number(self) -> int:
        return self.table_number

    def get_items(self) -> list[OrderItem]:
        return self.items

    def get_ordered_by(self) -> Customer:
        return self.ordered_by

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)

    def remove_item(self, item: OrderItem) -> None:
        self.items.remove(item)

    def get_total_price(self) -> float:
        return sum(item.get_subtotal() for item in self.items)
