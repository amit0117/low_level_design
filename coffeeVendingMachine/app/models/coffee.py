from app.models.enums import CoffeeType
from app.models.ingredient import Ingredient
from app.models.enums import IngredientType


class Coffee:
    def __init__(self, type: CoffeeType):
        self.type = type
        self.recipe: list[Ingredient] = []
        self.price: float | None = None  # in INR

    def grind_beans(self):
        print(f"Grinding beans for {self.type.value}")

    def pour_into_cup(self):
        print(f"Pouring Coffee of type {self.type.value} into a cup")

    def brew(self):
        # Brew is a process of making a beverage made through a biological and thermal process involving steeping, boiling, and fermenting.
        # Specifically distinguished from distilling, which is a physical process of concentration
        raise NotImplementedError("This method is not implemented")

    def add_condiments(self):
        # Condiments are the additional ingredients that are added to the coffee to enhance the flavor and taste.
        # For example, milk, sugar, cream, etc.
        # In general food, Condiments are the additional ingredients that are added to the food after it is cooked ,to enhance the flavor and taste.
        # Eg:Ketchup, Mustard, Green Chutney, etc.
        pass

    # Template method pattern
    def prepare(self):
        from time import sleep

        self.grind_beans()
        sleep(1)
        self.brew()
        sleep(1)
        self.add_condiments()
        sleep(1)
        self.pour_into_cup()
        sleep(1)

    def get_coffee_type(self) -> CoffeeType:
        return self.type

    def get_price(self) -> float:
        return self.price

    def get_recipe(self) -> list[Ingredient]:
        return self.recipe.copy()


class Espresso(Coffee):
    def __init__(self):
        super().__init__(CoffeeType.ESPRESSO)
        self.recipe = [Ingredient(IngredientType.COFFEE_BEANS.value, 10), Ingredient(IngredientType.WATER.value, 30)]
        self.price = 50

    def brew(self):
        print(f"Brewing Espresso under high pressure")


class Cappuccino(Coffee):
    def __init__(self):
        super().__init__(CoffeeType.CAPPUCCINO)
        self.recipe = [
            Ingredient(IngredientType.COFFEE_BEANS.value, 10),
            Ingredient(IngredientType.WATER.value, 10),
            Ingredient(IngredientType.MILK.value, 10),
        ]
        self.price = 70

    def brew(self):
        print(f"Brewing Cappuccino with hot water and coffee beans")

    def add_condiments(self):
        print(f"Adding milk to Cappuccino")


class Latte(Coffee):
    def __init__(self):
        super().__init__(CoffeeType.LATTE)
        self.recipe = [
            Ingredient(IngredientType.COFFEE_BEANS.value, 10),
            Ingredient(IngredientType.WATER.value, 10),
            Ingredient(IngredientType.MILK.value, 20),
        ]
        self.price = 80

    def brew(self):
        print(f"Brewing Latte with hot water and coffee beans")

    def add_condiments(self):
        print(f"Adding milk to Latte")
        print(f"Adding foam to Latte")
