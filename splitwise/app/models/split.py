from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class Split:
    def __init__(self, user: "User", amount: float):
        self.user = user
        self.amount = amount

    def get_user(self):
        return self.user

    def get_amount(self):
        return self.amount

    def set_amount(self, amount: float):
        self.amount = amount
