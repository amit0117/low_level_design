from app.observers.base_observer import BaseObserver
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.auction import Auction
    from app.models.bid import Bid


class AuctionObserver(BaseObserver):
    def update_on_auction_status_change(self, auction: "Auction"):
        print(f"Auction status changed to {auction.get_status().value}\n")

    def update_on_bid(self, bid: "Bid", message: Optional[str] = None):
        if not message:
            message = f"New Bid placed by {bid.get_user().get_name()} for {bid.get_amount()} on {bid.get_auction().get_item().get_name()}\n"
        print(message)


class AuctionSubject:
    def __init__(self):
        self.observers: list[BaseObserver] = []

    def add_observer(self, observer: BaseObserver):
        self.observers.append(observer)

    def remove_observer(self, observer: BaseObserver):
        self.observers.remove(observer)

    def notify_observers_on_auction_status_change(self, auction: "Auction"):
        for observer in self.observers:
            observer.update_on_auction_status_change(auction)

    def notify_observers_on_bid(self, bid: "Bid", message: Optional[str] = None):
        for observer in self.observers:
            observer.update_on_bid(bid, message)
