from abc import ABC, abstractmethod
from app.models.coffee import Coffee
from app.models.enums import CoffeeType, IngredientType
from app.models.ingredient import Ingredient


class CoffeeDecorator(Coffee, ABC):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def grind_beans(self):
        self._coffee.grind_beans()

    def pour_into_cup(self):
        self._coffee.pour_into_cup()

    def brew(self):
        self._coffee.brew()

    def prepare(self):
        self._coffee.prepare()

    def get_coffee_type(self) -> CoffeeType:
        return self._coffee.get_coffee_type()

    def get_price(self) -> float:
        base_price = self._coffee.get_price()
        if base_price is None:
            base_price = 0
        return base_price + self._get_extra_price()

    def get_recipe(self) -> list[Ingredient]:
        recipe = self._coffee.get_recipe().copy()
        extra_ingredients = self._get_extra_ingredients()

        recipe_dict = {}
        for ing in recipe:
            name_lower = ing.get_name().lower()
            recipe_dict[name_lower] = ing.get_quantity()

        for ing in extra_ingredients:
            name_lower = ing.get_name().lower()
            if name_lower in recipe_dict:
                recipe_dict[name_lower] += ing.get_quantity()
            else:
                recipe_dict[name_lower] = ing.get_quantity()

        result = []
        seen_names = set()
        for ing in recipe:
            name_lower = ing.get_name().lower()
            if name_lower not in seen_names:
                result.append(Ingredient(ing.get_name(), recipe_dict[name_lower]))
                seen_names.add(name_lower)

        for ing in extra_ingredients:
            name_lower = ing.get_name().lower()
            if name_lower not in seen_names:
                result.append(Ingredient(ing.get_name(), recipe_dict[name_lower]))
                seen_names.add(name_lower)

        return result

    def add_condiments(self) -> None:
        self._coffee.add_condiments()
        self._add_decorator_condiments()

    @abstractmethod
    def _get_extra_price(self) -> float:
        raise NotImplementedError("This method is not implemented")

    @abstractmethod
    def _get_extra_ingredients(self) -> list[Ingredient]:
        raise NotImplementedError("This method is not implemented")

    @abstractmethod
    def _add_decorator_condiments(self):
        raise NotImplementedError("This method is not implemented")


class SugarDecorator(CoffeeDecorator):
    def __init__(self, coffee: Coffee):
        super().__init__(coffee)
        self._extra_price = 5
        self._extra_ingredients = [Ingredient(IngredientType.SUGAR.value, 1)]

    def _get_extra_price(self) -> float:
        return self._extra_price

    def _get_extra_ingredients(self) -> list[Ingredient]:
        return self._extra_ingredients.copy()

    def _add_decorator_condiments(self):
        print(f"Adding sugar to {self.get_coffee_type().value}")


class ExtraMilkDecorator(CoffeeDecorator):
    def __init__(self, coffee: Coffee):
        super().__init__(coffee)
        self._extra_price = 10
        self._extra_ingredients = [Ingredient(IngredientType.MILK.value, 5)]

    def _get_extra_price(self) -> float:
        return self._extra_price

    def _get_extra_ingredients(self) -> list[Ingredient]:
        return self._extra_ingredients.copy()

    def _add_decorator_condiments(self):
        print(f"Adding extra milk to {self.get_coffee_type().value}")


class CreamDecorator(CoffeeDecorator):
    def __init__(self, coffee: Coffee):
        super().__init__(coffee)
        self._extra_price = 15
        self._extra_ingredients = [Ingredient(IngredientType.CREAM.value, 1)]

    def _get_extra_price(self) -> float:
        return self._extra_price

    def _get_extra_ingredients(self) -> list[Ingredient]:
        return self._extra_ingredients.copy()

    def _add_decorator_condiments(self):
        print(f"Adding cream to {self.get_coffee_type().value}")


class CaramelDecorator(CoffeeDecorator):
    def __init__(self, coffee: Coffee):
        super().__init__(coffee)
        self._extra_price = 8
        self._extra_ingredients = [Ingredient(IngredientType.CARAMEL_SYRUP.value, 1)]

    def _get_extra_price(self) -> float:
        return self._extra_price

    def _get_extra_ingredients(self) -> list[Ingredient]:
        return self._extra_ingredients.copy()

    def _add_decorator_condiments(self):
        print(f"Adding cream to {self.get_coffee_type().value}")
