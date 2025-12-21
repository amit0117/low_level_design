from app.models.enums import CoffeeType
from app.factories.coffee_factory import CoffeeFactory


class Menu:
    @staticmethod
    def display():
        menu_items = []
        for coffee_type in CoffeeType:
            coffee = CoffeeFactory.create_coffee(coffee_type)
            menu_items.append((coffee_type, coffee.get_price()))
        return menu_items
