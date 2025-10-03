from typing import List, Optional, Dict
from threading import Lock
from app.models.order import Order
from app.models.enums import OrderItemStatus


class OrderRepository:
    """Repository for order data access operations - Single Responsibility: Order persistence"""

    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.orders: Dict[str, Order] = {}
            self.data_lock = Lock()
            self._initialized = True

    def save(self, order: Order) -> None:
        """Save order to storage"""
        with self.data_lock:
            self.orders[order.get_order_id()] = order

    def find_by_id(self, order_id: str) -> Optional[Order]:
        """Find order by ID"""
        return self.orders.get(order_id)

    def find_all(self) -> List[Order]:
        """Get all orders"""
        return list(self.orders.values())

    def find_by_table(self, table_number: int) -> List[Order]:
        """Find orders by table number"""
        return [order for order in self.orders.values() if order.get_table_number() == table_number]

    def find_active_orders(self) -> List[Order]:
        """Get all active orders"""
        active_statuses = [OrderItemStatus.ORDERED, OrderItemStatus.PREPARING, OrderItemStatus.READY_FOR_PICKUP]
        return [order for order in self.orders.values() if any(item.get_status() in active_statuses for item in order.get_items())]

    def update(self, order: Order) -> None:
        """Update order in storage"""
        with self.data_lock:
            self.orders[order.get_order_id()] = order

    def delete(self, order_id: str) -> bool:
        """Delete order from storage"""
        with self.data_lock:
            if order_id in self.orders:
                del self.orders[order_id]
                return True
            return False
