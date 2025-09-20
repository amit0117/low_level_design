from app.models.order_item import OrderItem
from app.models.enums import OrderStatus
from app.models.observers.order_observer import OrderSubject, CustomerOrderObserver, AdminOrderObserver, WarehouseOrderObserver
from app.models.order_states import PendingState
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.order_states import OrderState


# add __repr__ and observers
class Order(OrderSubject):
    def __init__(self, user: "User") -> None:
        super().__init__()
        self.order_id = str(uuid.uuid4())
        self.order_items: list[OrderItem] = []
        self.owner = user
        self.status = OrderStatus.PENDING
        self.state: "OrderState" = PendingState()
        # we will add observers in the constructor
        self.add_observer(CustomerOrderObserver())
        self.add_observer(AdminOrderObserver())
        self.add_observer(WarehouseOrderObserver())
        # Add user as well to the observer list
        self.add_observer(user)

    def __repr__(self) -> str:
        return f"Order( id={self.order_id}, user={self.owner}, status={self.status}, state={self.state}, order_items={self.order_items})"

    def get_order_id(self) -> str:
        return self.order_id

    def add_order_item(self, order_item: OrderItem) -> None:
        self.order_items.append(order_item)

    def remove_order_item(self, order_item: OrderItem) -> None:
        if order_item not in self.order_items:
            print(f"Order item {order_item} not found in the order {self.order_id}")
            return
        self.order_items.remove(order_item)

    def get_order_items(self) -> list[OrderItem]:
        return self.order_items

    def get_owner(self) -> "User":
        return self.owner

    def get_status(self) -> OrderStatus:
        return self.status

    def get_state(self) -> "OrderState":
        return self.state

    def set_state(self, state: "OrderState") -> None:
        self.state = state

    def set_status(self, status: OrderStatus) -> None:
        self.status = status
        self.notify_observers(self)

    def ship(self) -> None:
        self.state.ship(self)
        self.notify_observers(self)

    def deliver(self) -> None:
        self.state.deliver(self)
        self.notify_observers(self)

    def cancel(self) -> None:
        self.state.cancel(self)
        self.notify_observers(self)

    def get_total_price(self) -> float:
        return sum(item.get_price() for item in self.order_items)
