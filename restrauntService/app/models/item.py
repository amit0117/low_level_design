from app.models.enums import MenuCategory
from uuid import uuid4


class Item:
    def __init__(self, name: str, price: float, category: MenuCategory):
        self.id = str(uuid4())
        self.name = name
        self.price = price
        self.category = category

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_category(self):
        return self.category


class VegItem(Item):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, MenuCategory.VEG)


class NonVegItem(Item):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, MenuCategory.NON_VEG)
