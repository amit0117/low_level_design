from uuid import uuid4
from app.observers.auction_observer import AuctionObserver
from app.mediator.auction_component import AuctionComponent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.bid import Bid
    from app.models.auction import Auction


class User(AuctionObserver, AuctionComponent):
    def __init__(self, name: str, email: str, password: str):
        AuctionObserver.__init__(self)
        AuctionComponent.__init__(self)
        self.id = str(uuid4())
        self.name = name
        self.email = email
        self.bidding_history: list["Bid"] = []
        self.auction_history: list["Auction"] = []
        self.password = password

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_email(self) -> str:
        return self.email

    def is_valid_password(self, password: str) -> bool:
        return self.password == password

    def get_bidding_history(self) -> list["Bid"]:
        return self.bidding_history

    def add_to_bidding_history(self, bid: "Bid"):
        self.bidding_history.append(bid)

    def remove_from_bidding_history(self, bid: "Bid"):
        self.bidding_history.remove(bid)

    def place_bid_on_auction(self, bid: "Bid") -> bool:
        """Place a bid on an auction through the mediator"""
        if not self._mediator:
            print(f"No mediator registered for user {self.get_name()}")
            return False

        return self._mediator.handle_bid_placement(bid)

    def remove_bid_from_auction(self, bid: "Bid") -> bool:
        """Remove a bid from an auction through the mediator"""
        if not self._mediator:
            print(f"No mediator registered for user {self.get_name()}")
            return False

        return self._mediator.handle_bid_removal(bid)

    def add_auction_to_history(self, auction: "Auction"):
        self.auction_history.append(auction)

    def remove_auction_from_history(self, auction: "Auction"):
        self.auction_history.remove(auction)

    def get_auction_history(self) -> list["Auction"]:
        return self.auction_history
