from app.models.product import Product
from typing import Optional, Dict
from threading import Lock
from app.models.enums import ProductStatus, UserType
from app.models.observers.inventory_observer import InventorySubject, InventoryObserver


class InventoryService(InventorySubject):
    """Inventory service that manages product stock and notifies observers about stock changes"""

    def __init__(self):
        super().__init__()
        # Store product objects and their stock counts
        self.products: Dict[str, Product] = {}
        self.stock_counts: Dict[str, int] = {}
        self.lock = Lock()
        self.subject = InventorySubject()

    def add_product(self, product: Product, initial_stock: int = 0) -> None:
        """Add a product to inventory with initial stock"""
        with self.lock:
            product_id = product.get_product_id()
            self.products[product_id] = product
            self.stock_counts[product_id] = initial_stock
            # Notify observers about new product availability
            if initial_stock > 0:
                self._notify_stock_change(UserType.NORMAL_USER, product, initial_stock)

    def remove_product(self, product: Product) -> None:
        """Remove a product from inventory"""
        with self.lock:
            product_id = product.get_product_id()
            if product_id not in self.products:
                print(f"Product with id {product_id} not found in inventory")
                return
            self.products.pop(product_id)
            self.stock_counts.pop(product_id)

    def get_product(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        return self.products.get(product_id)

    def get_product_stock_count(self, product_id: str) -> Optional[int]:
        """Get current stock count for a product"""
        if product_id not in self.stock_counts:
            print(f"Product with id {product_id} not found")
            return None
        return self.stock_counts[product_id]

    def update_stock(self, product_id: str, quantity: int) -> None:
        """Update stock for a product and notify observers about changes"""
        with self.lock:
            if product_id not in self.products:
                print(f"Product {product_id} not found in inventory")
                return

            product = self.products[product_id]
            old_stock = self.stock_counts[product_id]
            new_stock = old_stock + quantity

            # Update stock count
            self.stock_counts[product_id] = new_stock

            # Determine what type of notification to send
            if old_stock <= 0 and new_stock > 0:
                # Out of stock to in stock - notify all users
                self._notify_stock_change(UserType.NORMAL_USER, product, new_stock)
            elif old_stock > 0 and new_stock <= 0:
                # In stock to out of stock - notify admin
                self._notify_stock_change(UserType.ADMIN, product, new_stock)

    def is_product_available(self, product_id: str) -> bool:
        """Check if product is available (in stock)"""
        if product_id not in self.stock_counts:
            return False
        return self.stock_counts[product_id] > 0

    def get_available_products(self) -> list[Product]:
        """Get all available products"""
        return [product for product_id, product in self.products.items() if self.is_product_available(product_id)]

    def get_out_of_stock_products(self) -> list[Product]:
        """Get all out of stock products"""
        return [product for product_id, product in self.products.items() if not self.is_product_available(product_id)]

    def _notify_stock_change(self, user_type: UserType, product: Product, new_stock: int) -> None:
        """Notify observers about stock changes"""
        # Update product's stock status based on new stock count
        if new_stock <= 0:
            product.set_status(ProductStatus.OUT_OF_STOCK)
        else:
            product.set_status(ProductStatus.AVAILABLE)

        # Notify all observers
        self.subject.notify_observers(user_type, product)

    def add_observer(self, observer: InventoryObserver) -> None:
        """Add an inventory observer"""
        self.subject.add_observer(observer)
        print(f"Added inventory observer: {type(observer).__name__}")

    def remove_observer(self, observer: InventoryObserver) -> None:
        """Remove an inventory observer"""
        self.subject.remove_observer(observer)
        print(f"Removed inventory observer: {type(observer).__name__}")

    def get_inventory_summary(self) -> Dict[str, Dict]:
        """Get summary of all products in inventory"""
        summary = {}
        for product_id, product in self.products.items():
            stock_count = self.stock_counts[product_id]
            summary[product_id] = {
                "name": product.get_name(),
                "price": product.get_price(),
                "category": product.get_category().value,
                "stock": stock_count,
                "status": product.get_status().value,
                "available": self.is_product_available(product_id),
            }
        return summary
