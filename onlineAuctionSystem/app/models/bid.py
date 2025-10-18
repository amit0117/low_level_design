from uuid import uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.auction import Auction


class Bid:
    def __init__(self, user: "User", auction: "Auction", amount: float):
        self.id = str(uuid4())
        self.user = user
        self.amount = amount
        self.auction = auction

    def get_id(self) -> str:
        return self.id

    def get_user(self) -> "User":
        return self.user

    def get_amount(self) -> float:
        return self.amount

    def get_auction(self) -> "Auction":
        return self.auction
