from threading import Lock
from typing import Optional
from app.observers.inventory.subject import InventorySubject
from app.models.ingredient import Ingredient


class Inventory(InventorySubject):
    _instance: Optional["Inventory"] = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._has_initialized = False
        return cls._instance

    def __init__(self):
        if self._has_initialized:
            return
        InventorySubject.__init__(self)
        self.ingredients: dict[str, Ingredient] = {}
        self.lock = Lock()
        self._has_initialized = True
        self.threshold_quantity = 2
        self.processing_lock = Lock()

    @classmethod
    def get_instance(cls) -> "Inventory":
        return cls._instance or cls()

    def add_item(self, item: str, quantity: int) -> None:
        with self.processing_lock:
            ingredient = self.ingredients.get(item.lower())
            if not ingredient:
                ingredient = Ingredient(item, quantity)
                self.ingredients[item.lower()] = ingredient
            else:
                ingredient.update_quantity(quantity)

    def remove_item(self, item: str, quantity: int) -> None:
        with self.processing_lock:
            ingredient = self.ingredients.get(item.lower())
            if not ingredient:
                print(f"Item {item} not found in inventory")
                return
            ingredient.update_quantity(-quantity)

            # Notify observers if the quantity is less than the threshold quantity
            if ingredient.get_quantity() <= self.threshold_quantity:
                self.notify_observers(ingredient.get_name(), ingredient.get_quantity())

    def get_unavailable_items(self) -> list[str]:
        return [ingredient.get_name() for ingredient in self.ingredients.values() if ingredient.get_quantity() <= 0]

    def get_status(self) -> dict:
        return {
            "total_items": len(self.ingredients),
            "available_items": [ingredient.get_name() for ingredient in self.ingredients.values() if ingredient.get_quantity() > 0],
            "out_of_stock_items": self.get_unavailable_items(),
        }

    def has_sufficient_ingredients(self, ingredients: list[Ingredient]) -> bool:
        for ingredient in ingredients:
            if not self.ingredients.get(ingredient.get_name().lower()):
                print(f"Ingredient {ingredient.get_name()} not found in inventory")
                return False
            if self.ingredients[ingredient.get_name().lower()].get_quantity() < ingredient.get_quantity():
                print(f"Ingredient {ingredient.get_name()} has insufficient quantity in inventory")
                return False
        return True

    def check_availability(self, recipe: list[Ingredient]) -> bool:
        return self.has_sufficient_ingredients(recipe)

    def consume_ingredients(self, recipe: list[Ingredient]) -> None:
        for ingredient in recipe:
            self.remove_item(ingredient.get_name(), ingredient.get_quantity())
