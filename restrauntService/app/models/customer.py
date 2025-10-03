from app.observers.order_observer import OrderObserver
from app.observers.table_observer import TableObserver


class Customer(OrderObserver, TableObserver):
    def __init__(self, name: str) -> None:
        OrderObserver.__init__(self)
        TableObserver.__init__(self, None)  # Customer doesn't need a specific table initially
        self.name = name

    def get_name(self) -> str:
        return self.name

    def update_order_status(self, order) -> None:
        print(f"Customer {self.name} notified: Order {order.get_order_id()} status updated")

    def update_table_status(self, table) -> None:
        print(f"Customer {self.name} notified: Table {table.get_table_number()} status updated to {table.get_status().value}")
