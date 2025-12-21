from enum import Enum


# Espresso is the most basic coffee type. It is made with only coffee and water.
# Cappuccino is a coffee type that is made with coffee, water, and milk(1:1:1).
# Latte is a coffee type that is made with coffee, water, and milk(1:1:2).
# Keep enums so that we can later add more coffee types easily(like Americano (1:1), etc.).
class CoffeeType(Enum):
    ESPRESSO = "ESPRESSO"
    CAPPUCCINO = "CAPPUCCINO"
    LATTE = "LATTE"


class IngredientType(Enum):
    COFFEE_BEANS = "COFFEE_BEANS"
    WATER = "WATER"
    MILK = "MILK"
    SUGAR = "SUGAR"
    CREAM = "CREAM"
    CARAMEL_SYRUP = "CARAMEL_SYRUP"  # A kind of sugar which generally used in Latte


class Coin(Enum):
    ONE = 1
    FIVE = 5
    TEN = 10
    TWENTY = 20
    FIFTY = 50
    HUNDRED = 100
    TWO_HUNDRED = 200
    FIVE_HUNDRED = 500
    THOUSAND = 1000
