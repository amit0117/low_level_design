from typing import TYPE_CHECKING
from threading import Lock

if TYPE_CHECKING:
    from app.models.user import User


class BalanceSheet:
    def __init__(self, user: "User"):
        self.owner = user
        # Will store the balances of the user with other users
        self.balances: dict["User", float] = {}
        self.lock = Lock()

    def get_balances(self):
        return self.balances

    def adjust_balance(self, user: "User", amount: float):
        if user == self.owner or amount == 0:
            return
        with self.lock:
            self.balances[user] = self.balances.get(user, 0) + amount
            # Check if the balance is zero, if so, remove the user from the balances
            if self.balances[user] == 0:
                del self.balances[user]

    def show_balances(self):
        print(f"\nBalance Sheet for {self.owner.get_name()}:")
        if len(self.balances) == 0:
            print("All settled up!")
            return

        total_owed_to_me = 0
        total_i_owe = 0

        for user, amount in self.balances.items():
            if amount > 0:
                total_owed_to_me += amount
                print(f"{user.get_name()} owes {self.owner.get_name()} {amount}")
            else:
                total_i_owe += amount
                print(f"{self.owner.get_name()} owes {user.get_name()} {amount}")
        print("---------------------------------")
        print(f"Total Owed to {self.owner.get_name()}: {total_owed_to_me}")
        print(f"Total {self.owner.get_name()} Owes: {total_i_owe}")
        print("---------------------------------\n")
