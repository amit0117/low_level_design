from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.auction import Auction
    from app.models.bid import Bid


class BaseObserver(ABC):
    @abstractmethod
    def update_on_auction_status_change(self, auction: "Auction"):
        raise NotImplementedError("update_on_auction_status_change method has not been implemented")

    @abstractmethod
    def update_on_bid(self, bid: "Bid"):
        raise NotImplementedError("update_on_bid method has not been implemented")
