from app.models.item import Item
from app.models.enums import OrderItemStatus
from app.states.order_item_state import OrderedState, OrderItemState


class OrderItem:
    def __init__(self, order_id: str, item: Item, quantity: int) -> None:
        self.order_id = order_id
        self.item = item
        self.quantity = quantity
        self.status = OrderItemStatus.ORDERED
        self.state = OrderedState()

    def get_state(self) -> OrderItemState:
        return self.state

    def set_state(self, state: OrderItemState) -> None:
        self.state = state

    def get_status(self) -> OrderItemStatus:
        return self.status

    def set_status(self, status: OrderItemStatus) -> None:
        self.status = status

    def get_order_id(self) -> str:
        return self.order_id

    def get_item(self) -> Item:
        return self.item

    def get_quantity(self) -> int:
        return self.quantity

    def update_quantity(self, quantity: int) -> None:
        self.quantity = quantity

    def get_subtotal(self) -> float:
        return self.item.get_price() * self.quantity

    def start_preparation(self) -> None:
        self.state.start_preparation(self)

    def make_ready_for_pickup(self) -> None:
        self.state.make_ready_for_pickup(self)

    def serve_item(self) -> None:
        self.state.serve_item(self)

    def cancel_order_item(self) -> None:
        self.state.cancel_order_item(self)

    def __str__(self) -> str:
        return f"{self.item.get_name()} x {self.quantity} = {self.get_subtotal()}"
