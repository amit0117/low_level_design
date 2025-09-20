from typing import List, Optional
from app.models.order import Order
from app.models.user import User
from app.models.order_item import OrderItem
from app.models.enums import OrderStatus
from app.models.cart_item import CartItem


class OrderService:
    """Service for managing orders - focused only on order CRUD operations"""

    def __init__(self):
        self.orders: dict[str, Order] = {}

    def create_order_from_cart(self, user: User, cart_items: list[CartItem]) -> Optional[Order]:
        """Create a new order from cart items"""
        if not cart_items:
            print("Cart items are empty")
            return None

        order = Order(user)

        # Add order items from cart
        for item in cart_items:
            order_item = OrderItem(product_id=item.get_product().get_product_id(), quantity=item.get_quantity(), price=item.get_price())
            order.add_order_item(order_item)

        self.orders[order.get_order_id()] = order
        return order

    def get_order(self, order_id: str) -> Optional[Order]:
        """Get order by ID"""
        if order_id not in self.orders:
            print(f"Order with id {order_id} not found")
            return None
        return self.orders.get(order_id)

    def get_orders_by_user(self, user_id: str) -> List[Order]:
        """Get all orders for a specific user"""
        return [order for order in self.orders.values() if order.get_owner().get_user_id() == user_id]

    def update_order_status(self, order_id: str, status: OrderStatus) -> bool:
        """Update order status"""
        order = self.get_order(order_id)
        if order:
            order.set_status(status)
            return True
        print(f"Order with id {order_id} not found in order service")
        return False

    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        order = self.get_order(order_id)
        if order:
            order.cancel()
            return True
        print(f"Order with id {order_id} not found in order service")
        return False

    def ship_order(self, order_id: str) -> bool:
        """Ship an order"""
        order = self.get_order(order_id)
        if order:
            order.ship()
            return True
        return False

    def deliver_order(self, order_id: str) -> bool:
        """Mark order as delivered"""
        order = self.get_order(order_id)
        if order:
            order.deliver()
            return True
        return False

    def get_all_orders(self) -> List[Order]:
        """Get all orders"""
        return list(self.orders.values())

    def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        """Get orders by status"""
        return [order for order in self.orders.values() if order.get_status() == status]
