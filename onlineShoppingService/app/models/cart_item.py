from app.models.product import Product


class CartItem:
    def __init__(self, product: Product, quantity: int) -> None:
        self.product = product
        self.quantity = quantity

    def get_product(self) -> Product:
        return self.product

    def get_quantity(self) -> int:
        return self.quantity

    def get_price(self) -> float:
        return self.product.get_price() * self.quantity

    def increment_quantity(self, amount: int = 1) -> None:
        if amount < 0:
            print(f"Quantity cannot be negative for {self.product.get_name()}")
            return
        self.quantity += amount

    def decrement_quantity(self, amount: int = 1) -> None:
        if self.quantity - amount < 0:
            print(f"Quantity cannot be negative for {self.product.get_name()}")
            return
        self.quantity -= amount

    def __repr__(self) -> str:
        return f"{self.product.get_name()} x {self.quantity}"
