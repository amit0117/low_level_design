from uuid import uuid4
from app.models.enums import ProductCategory, ProductStatus
from app.models.observers.inventory_observer import InventorySubject


class Product(InventorySubject):
    def __init__(self, name: str, price: float, description: str, category: ProductCategory) -> None:
        self.product_id = str(uuid4())
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.status = ProductStatus.AVAILABLE

    def get_product_id(self) -> str:
        return self.product_id

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.price

    def get_description(self) -> str:
        return self.description

    def get_category(self) -> ProductCategory:
        return self.category

    def get_status(self) -> ProductStatus:
        return self.status

    def set_status(self, status: ProductStatus) -> None:
        self.status = status

    def is_available(self) -> bool:
        return self.status == ProductStatus.AVAILABLE

    def __repr__(self) -> str:
        return f"Product( id={self.product_id}, name={self.name}, price={self.price}, description={self.description}, category={self.category})"


# add __repr__ and observers
