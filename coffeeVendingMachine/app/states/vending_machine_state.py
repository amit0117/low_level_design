from abc import ABC, abstractmethod
from app.models.enums import CoffeeType, Coin
from app.models.inventory import Inventory
from app.services.transaction_service import TransactionService
from typing import TYPE_CHECKING
from app.models.coffee import Coffee

if TYPE_CHECKING:
    from app.models.vending_machine import VendingMachine


class VendingMachineState(ABC):
    def __init__(self, vending_machine: "VendingMachine"):
        self.vending_machine = vending_machine
        self.transaction_service = TransactionService()

    @abstractmethod
    def insert_coin(self, coin: Coin) -> None:
        pass

    @abstractmethod
    def select_coffee_type(self, coffee_type: CoffeeType) -> None:
        pass

    @abstractmethod
    def dispense_coffee(self) -> None:
        pass

    @abstractmethod
    def return_change(self) -> None:
        pass

    @abstractmethod
    def cancel(self) -> None:
        pass

    def __str__(self) -> str:
        return self.__class__.__name__

    def reset_machine(self) -> None:
        self.vending_machine.inserted_coins.clear()
        self.vending_machine.selected_coffee_type = None
        self.vending_machine.current_coffee = None
        self.vending_machine.coffee_decorators = []


class ReadyState(VendingMachineState):
    def insert_coin(self, coin: Coin) -> None:
        self.vending_machine.inserted_coins.append(coin)
        self.vending_machine.set_state(CashCollectedState(self.vending_machine))

    def select_coffee_type(self, coffee_type: CoffeeType) -> None:
        print("Invalid: Please insert cash first before selecting a coffee type.")

    def dispense_coffee(self) -> None:
        print("Invalid: Please insert cash and select a coffee type first.")

    def return_change(self) -> None:
        print("Invalid: No transaction in progress. No change to return.")

    def cancel(self) -> None:
        print("Invalid: No transaction in progress to cancel.")


class CashCollectedState(VendingMachineState):
    def insert_coin(self, coin: Coin) -> None:
        self.vending_machine.inserted_coins.append(coin)

    def select_coffee_type(self, coffee_type: CoffeeType) -> None:
        self.vending_machine.selected_coffee_type = coffee_type
        coffee = self.vending_machine.create_coffee_with_decorators(coffee_type)
        self.vending_machine.current_coffee = coffee

        price = coffee.get_price()
        is_valid, paid_amount = self.transaction_service.validate_payment(price, self.vending_machine.inserted_coins)

        if not is_valid:
            print(f"Invalid: Insufficient payment. Required: {price} INR, Paid: {paid_amount} INR")
            return

        inventory = Inventory.get_instance()
        if not inventory.check_availability(coffee.get_recipe()):
            print(f"Invalid: Cannot prepare {coffee_type.value}. Insufficient ingredients in inventory.")
            self.reset_machine()
            self.vending_machine.set_state(TransactionCancelledState(self.vending_machine))
            return

        dispense_state = DispenseItemState(self.vending_machine)
        self.vending_machine.set_state(dispense_state)
        dispense_state.dispense_coffee()

    def dispense_coffee(self) -> None:
        print("Invalid: Please select a coffee type first.")

    def return_change(self) -> None:
        print("Invalid: Please complete the transaction first.")

    def cancel(self) -> None:
        self.reset_machine()
        self.vending_machine.set_state(TransactionCancelledState(self.vending_machine))


class DispenseItemState(VendingMachineState):
    def insert_coin(self, coin: Coin) -> None:
        print("Invalid: Transaction in progress. Please wait for the current transaction to complete.")

    def select_coffee_type(self, coffee_type: CoffeeType) -> None:
        print("Invalid: Transaction in progress. Cannot change selection.")

    def dispense_coffee(self) -> None:
        if not self.vending_machine.current_coffee:
            print("Invalid: No coffee selected to dispense.")
            return

        coffee: Coffee = self.vending_machine.current_coffee
        inventory: Inventory = Inventory.get_instance()
        inventory.consume_ingredients(coffee.get_recipe())
        coffee.prepare()

        price = coffee.get_price()
        total_paid = self.vending_machine.get_total_paid()
        change = self.transaction_service.calculate_change(total_paid, price)

        if change > 0:
            change_state = DispenseChangeState(self.vending_machine, change)
            self.vending_machine.set_state(change_state)
            change_state.return_change()
        else:
            self.vending_machine.set_state(ReadyState(self.vending_machine))

        # Reset the machine
        self.reset_machine()

    def return_change(self) -> None:
        print("Invalid: Please wait for the coffee to be dispensed first.")

    def cancel(self) -> None:
        print("Invalid: Cannot cancel transaction while dispensing. Please wait for completion.")


class DispenseChangeState(VendingMachineState):
    def __init__(self, vending_machine: "VendingMachine", change_amount: float):
        super().__init__(vending_machine)
        self.change_amount = change_amount

    def insert_coin(self, coin: Coin) -> None:
        print("Invalid: Please wait for change to be returned.")

    def select_coffee_type(self, coffee_type: CoffeeType) -> None:
        print("Invalid: Please wait for change to be returned.")

    def dispense_coffee(self) -> None:
        print("Invalid: Coffee has already been dispensed.")

    def return_change(self) -> None:
        print(f"Returning change: {self.change_amount} INR")
        self.vending_machine.set_state(ReadyState(self.vending_machine))

    def cancel(self) -> None:
        print("Invalid: Please wait for change to be returned.")


class TransactionCancelledState(VendingMachineState):
    def insert_coin(self, coin: Coin) -> None:
        print("Invalid: Previous transaction was cancelled. Please start a new transaction.")

    def select_coffee_type(self, coffee_type: CoffeeType) -> None:
        print("Invalid: Previous transaction was cancelled. Please start a new transaction.")

    def dispense_coffee(self) -> None:
        print("Invalid: Transaction was cancelled. No coffee to dispense.")

    def return_change(self) -> None:
        self.vending_machine.set_state(ReadyState(self.vending_machine))

    def cancel(self) -> None:
        self.vending_machine.set_state(ReadyState(self.vending_machine))
