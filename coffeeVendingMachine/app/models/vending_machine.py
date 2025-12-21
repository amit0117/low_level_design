from app.states.vending_machine_state import VendingMachineState, ReadyState
from app.models.enums import CoffeeType, Coin
from app.factories.coffee_factory import CoffeeFactory


class VendingMachine:
    def __init__(self):
        self.selected_coffee_type: CoffeeType | None = None
        self.inserted_coins: list[Coin] = []
        self.current_coffee = None
        self.coffee_decorators: list = []
        self.state: VendingMachineState = ReadyState(self)

    def set_state(self, state: VendingMachineState):
        self.state = state

    def get_state(self) -> VendingMachineState:
        return self.state

    def select_coffee_type(self, coffee_type: CoffeeType) -> None:
        self.state.select_coffee_type(coffee_type)

    def insert_coin(self, coin: Coin) -> None:
        self.state.insert_coin(coin)

    def return_change(self) -> None:
        self.state.return_change()

    def dispense_coffee(self) -> None:
        self.state.dispense_coffee()

    def cancel(self) -> None:
        self.state.cancel()

    def create_coffee_with_decorators(self, coffee_type: CoffeeType):
        coffee = CoffeeFactory.create_coffee(coffee_type)
        if self.coffee_decorators:
            for decorator_class in self.coffee_decorators:
                coffee = decorator_class(coffee)
        return coffee

    def get_total_paid(self) -> float:
        return sum(coin.value for coin in self.inserted_coins)

    def get_coffee_price(self) -> float | None:
        if not self.selected_coffee_type:
            return None

        coffee = CoffeeFactory.create_coffee(self.selected_coffee_type)
        return coffee.get_price()
