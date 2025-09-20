from app.models.product import Product
from app.services.inventory_service import InventoryService
from app.models.enums import ProductCategory
from typing import Any


class SearchStrategy:
    def __init__(self):
        self.inventory_service = InventoryService()

    def search(self, query: Any) -> list[Product]:
        raise NotImplementedError("Subclasses must implement this method")


class SearchByNameStrategy(SearchStrategy):

    def search(self, query: str) -> list[Product]:
        return [product for product in self.inventory_service.get_available_products() if query.lower() in product.get_name().lower()]


class SearchByCategoryStrategy(SearchStrategy):

    def search(self, query_category: ProductCategory) -> list[Product]:
        return [product for product in self.inventory_service.get_available_products() if product.get_category().value == query_category.value]


class SearchByPriceRangeStrategy(SearchStrategy):

    def search(self, query_price_range: tuple[float, float]) -> list[Product]:
        return [
            product
            for product in self.inventory_service.get_available_products()
            if product.get_price() >= query_price_range[0] and product.get_price() <= query_price_range[1]
        ]
