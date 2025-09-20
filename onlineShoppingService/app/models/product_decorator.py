# Decorator pattern to add features to a product
from app.models.product import Product


class ProductDecorator(Product):
    def __init__(self, product: Product):
        self.product = product

    # Default implementation for the decorator to add features to a product
    def get_price(self) -> float:
        return self.product.get_price()

    def get_description(self) -> str:
        return self.product.get_description()


class GiftWrapperDecorator(ProductDecorator):
    def __init__(self, product: Product, gift_wrap_cost: float = 5.0):
        super().__init__(product)
        self.gift_wrap_cost = gift_wrap_cost

    def get_price(self) -> float:
        return self.product.get_price() + self.gift_wrap_cost

    def get_description(self) -> str:
        return self.product.get_description() + " (Gift Wrapped)"
