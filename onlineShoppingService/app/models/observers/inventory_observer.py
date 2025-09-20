from abc import ABC, abstractmethod
from app.models.enums import UserType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.product import Product


class InventoryObserver(ABC):
    @abstractmethod
    # when product is updated (like if stock is updated from out of stock to in stock (then notify all subscribed users and if stock <=0 then notify the admin))
    def update_about_stock(self, user_type: "UserType", product: "Product"):
        raise NotImplementedError("Subclass must implement this method")


# Concrete implementation of InventoryObserver (for out of stock to in stock), for user purpose
class OutOfStockToInStockObserver(InventoryObserver):
    def update_about_stock(self, user_type: "UserType", product: "Product"):
        if product.is_available():
            print(f"Product {product.get_name()} is now in stock")
        elif user_type == UserType.ADMIN:
            print(f"Product {product.get_name()} is out of stock")


# For Admin purpose
class InStockToOutOfStockObserver(InventoryObserver):
    def update_about_stock(self, user_type: "UserType", product: "Product"):
        if not product.is_available() and user_type == UserType.ADMIN:
            print(f"Product {product.get_name()} is now out of stock, notify the admin")


class InventorySubject:
    def __init__(self) -> None:
        self.observers: list[InventoryObserver] = []

    def add_observer(self, observer: InventoryObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: InventoryObserver) -> None:
        if observer in self.observers:
            self.observers.remove(observer)
            return
        print(f"Observer {observer.get_user_name()} not found in the inventory subject")

    def notify_observers(self, user_type: "UserType", product: "Product") -> None:
        for observer in self.observers:
            observer.update_about_stock(user_type, product)
