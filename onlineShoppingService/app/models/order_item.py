from app.models.product import Product


class OrderItem:
    def __init__(self, product_id: str, quantity: int, price: float):
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def get_product_id(self) -> str:
        return self.product_id

    def get_quantity(self) -> int:
        return self.quantity

    def get_price(self) -> float:
        return self.price

    def get_total_price(self) -> float:
        return self.price * self.quantity

    def __repr__(self) -> str:
        return f"OrderItem(product_id={self.product_id}, quantity={self.quantity}, price={self.price})"
