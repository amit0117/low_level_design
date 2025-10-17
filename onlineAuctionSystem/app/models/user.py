from uuid import uuid4
from app.models.bid import Bid
from app.observers.base_observer import BaseObserver
from app.mediator.auction_mediator import AuctionMediator


class User(BaseObserver, AuctionMediator):
    def __init__(self, name: str, email: str):
        super().__init__()
        self.id = str(uuid4())
        self.name = name
        self.email = email
        self.bidding_history: list[Bid] = []
        self.auction_mediator = AuctionMediator()

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_email(self) -> str:
        return self.email

    def get_bidding_history(self) -> list[Bid]:
        return self.bidding_history

    def add_to_bidding_history(self, bid: Bid):
        self.bidding_history.append(bid)
