from concurrent.futures import ThreadPoolExecutor
from app.models.vending_machine import VendingMachine
from app.models.enums import CoffeeType, Coin
from app.decorators.coffee_decorator import SugarDecorator, ExtraMilkDecorator, CaramelDecorator
from app.models.inventory import Inventory
from app.models.menu import Menu
from app.models.enums import IngredientType
from app.models.admin import Admin


def setup_inventory():
    inventory = Inventory.get_instance()
    inventory.add_item(IngredientType.COFFEE_BEANS.value, 100)
    inventory.add_item(IngredientType.WATER.value, 200)
    inventory.add_item(IngredientType.MILK.value, 150)
    inventory.add_item(IngredientType.SUGAR.value, 50)
    inventory.add_item(IngredientType.CREAM.value, 30)
    inventory.add_item(IngredientType.CARAMEL_SYRUP.value, 20)


def order_coffee(order_name: str, coffee_type: CoffeeType, decorators: list = None):
    machine = VendingMachine()

    Menu.display()

    if decorators:
        machine.coffee_decorators = decorators

    # First insert coins (Ready -> CashCollected)
    # Estimate price for coins needed
    temp_coffee = machine.create_coffee_with_decorators(coffee_type)
    price = temp_coffee.get_price()
    coins = [Coin.HUNDRED] if price <= 100 else [Coin.HUNDRED, Coin.HUNDRED]
    for coin in coins:
        machine.insert_coin(coin)

    # Then select coffee type (CashCollected -> DispenseItem -> DispenseChange -> Ready)
    # Note: select_coffee_type() automatically calls dispense_coffee() which automatically calls return_change() if change > 0
    machine.select_coffee_type(coffee_type)

    return f"{order_name} completed"


def demo():
    setup_inventory()

    orders = [
        ("LatteWithExtraSugar", CoffeeType.LATTE, [SugarDecorator]),
        ("LatteWithExtraMilk", CoffeeType.LATTE, [ExtraMilkDecorator]),
        ("LatteWithExtraSugarAndMilk", CoffeeType.LATTE, [SugarDecorator, ExtraMilkDecorator]),
        ("CappuccinoWithDoubleSugarAndCaramel", CoffeeType.CAPPUCCINO, [SugarDecorator, SugarDecorator, CaramelDecorator]),
    ]

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(order_coffee, name, coffee_type, decorators) for name, coffee_type, decorators in orders]

        for future in futures:
            result = future.result()


def demo_observer_pattern():
    print("\n=== Observer Pattern Demo: Admin Notifications ===")

    admin1 = Admin("Rajesh Kumar")
    admin2 = Admin("Priya Sharma")
    admin3 = Admin("Amit Patel")

    inventory = Inventory.get_instance()

    # Clear existing observers and add new ones
    inventory.observers.clear()
    inventory.add_observer(admin1)
    inventory.add_observer(admin2)
    inventory.add_observer(admin3)

    # Clear existing inventory by removing large quantities, then set low quantities
    # This ensures we start fresh for the observer demo
    for ingredient_name in [
        IngredientType.COFFEE_BEANS.value,
        IngredientType.WATER.value,
        IngredientType.MILK.value,
        IngredientType.SUGAR.value,
        IngredientType.CREAM.value,
        IngredientType.CARAMEL_SYRUP.value,
    ]:
        if ingredient_name.lower() in inventory.ingredients:
            existing_qty = inventory.ingredients[ingredient_name.lower()].get_quantity()
            if existing_qty > 0:
                inventory.remove_item(ingredient_name, existing_qty)

    # Set low quantities to trigger notifications
    # Latte: 10 beans, 10 water, 20 milk | Cappuccino: 10 beans, 10 water, 10 milk | Espresso: 10 beans, 30 water
    # Threshold = 2, so we need quantities to drop to 2 or below
    inventory.add_item(IngredientType.COFFEE_BEANS.value, 25)  # After 2 orders: 5, after 3: -5 (triggers)
    inventory.add_item(IngredientType.WATER.value, 50)  # After 2 Lattes: 30, after Cappuccino: 20, after Espresso: -10 (triggers)
    inventory.add_item(IngredientType.MILK.value, 42)  # After 1 Latte: 22, after 2: 2 (triggers!), after Cappuccino: -8 (triggers)
    inventory.add_item(IngredientType.SUGAR.value, 2)
    inventory.add_item(IngredientType.CREAM.value, 1)
    inventory.add_item(IngredientType.CARAMEL_SYRUP.value, 4)

    print("\nProcessing orders to trigger low inventory notifications...\n")

    orders = [CoffeeType.LATTE, CoffeeType.LATTE, CoffeeType.CAPPUCCINO, CoffeeType.ESPRESSO]

    for coffee_type in orders:
        machine = VendingMachine()
        temp_coffee = machine.create_coffee_with_decorators(coffee_type)
        price = temp_coffee.get_price()
        coins = [Coin.HUNDRED] if price <= 100 else [Coin.HUNDRED, Coin.HUNDRED]
        for coin in coins:
            machine.insert_coin(coin)
        machine.select_coffee_type(coffee_type)

    print("\nRemoving observer: Priya Sharma")
    inventory.remove_observer(admin2)

    print("Processing one more order (only 2 admins will be notified)...\n")
    machine = VendingMachine()
    temp_coffee = machine.create_coffee_with_decorators(CoffeeType.LATTE)
    price = temp_coffee.get_price()
    coins = [Coin.HUNDRED] if price <= 100 else [Coin.HUNDRED, Coin.HUNDRED]
    for coin in coins:
        machine.insert_coin(coin)
    machine.select_coffee_type(CoffeeType.LATTE)

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
    print("\n" + "=" * 60 + "\n")
    demo_observer_pattern()
    print("\n" + "=" * 60 + "\n")
