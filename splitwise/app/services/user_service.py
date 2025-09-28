from app.models.user import User
from typing import Optional


class UserService:
    def __init__(self):
        self.users: dict[str, User] = {}

    def create_user(self, name: str, email: str) -> User:
        user = User(name, email)
        self.users[user.get_id()] = user
        return user

    def get_user(self, id: str) -> Optional[User]:
        return self.users.get(id)

    def get_all_users(self) -> list[User]:
        return list(self.users.values())

    def settle_up(self, user_id1: str, user_id2: str, amount: float):
        if not all(user_id in self.users for user_id in [user_id1, user_id2]):
            raise ValueError(f"User with id {user_id1} or {user_id2} not found")

        user1 = self.users[user_id1]
        user2 = self.users[user_id2]
        print(f"\n{user1.get_name()} is settling up {amount} with {user2.get_name()}\n")
        # Just like a reverse expense
        user1.get_balance_sheet().adjust_balance(user2, -1 * amount)
        user2.get_balance_sheet().adjust_balance(user1, amount)

    def show_balance_sheet(self, user_id: str):
        if user_id not in self.users:
            raise ValueError(f"User with id {user_id} not found")
        user = self.users[user_id]
        user.get_balance_sheet().show_balances()
