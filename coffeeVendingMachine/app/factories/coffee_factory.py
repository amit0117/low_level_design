from app.models.enums import CoffeeType
from app.models.coffee import Coffee, Espresso, Cappuccino, Latte


class CoffeeFactory:
    @staticmethod
    def create_coffee(coffee_type: CoffeeType) -> Coffee:
        if coffee_type == CoffeeType.ESPRESSO:
            return Espresso()
        elif coffee_type == CoffeeType.CAPPUCCINO:
            return Cappuccino()
        elif coffee_type == CoffeeType.LATTE:
            return Latte()
