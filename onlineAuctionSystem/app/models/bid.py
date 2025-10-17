from uuid import uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.auction import Auction


class Bid:
    def __init__(self, user: "User", amount: float, item: "Auction"):
        self.id = str(uuid4())
        self.user = user
        self.amount = amount
        self.item = item

    def get_id(self) -> str:
        return self.id

    def get_user(self) -> "User":
        return self.user

    def get_amount(self) -> float:
        return self.amount

    def get_auction(self) -> "Auction":
        return self.item
