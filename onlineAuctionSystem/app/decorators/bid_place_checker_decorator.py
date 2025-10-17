from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.auction import Auction
    from app.models.bid import Bid


class AuctionDecorator(ABC):
    @abstractmethod
    def can_place_bid(self, auction: "Auction", bid: "Bid") -> bool:
        raise NotImplementedError("can_place_bid method has not been implemented")


class BaseAuctionDetector(AuctionDecorator):
    """Base class for auction detectors"""

    def can_place_bid(self, auction: "Auction", bid: "Bid") -> bool:
        return bid.get_auction() == auction and auction.is_active()


class OwnerCheckDecorator(AuctionDecorator):

    def can_place_bid(self, auction: "Auction", bid: "Bid") -> bool:
        if bid.get_user().get_id() == auction.get_owner().get_id():
            print(f"OwnerCheckDecorator: User {bid.get_user().get_id()} cannot place bid on auction {auction.get_id()} because they are the owner")
            return False
        return super().can_place_bid(auction, bid)


class FraudDetectionDecorator(AuctionDecorator):
    def __init__(self):
        self.max_bid_amount = 1000000
        self.min_bid_amount = 100

    def can_place_bid(self, auction: "Auction", bid: "Bid") -> bool:
        if bid.get_amount() > self.max_bid_amount:
            print(
                f"FraudDetector: User {bid.get_user().get_id()} cannot place bid on auction {auction.get_id()} because the bid amount is greater than the max bid amount"
            )
            return False
        if bid.get_amount() < self.min_bid_amount:
            print(
                f"FraudDetector: User {bid.get_user().get_id()} cannot place bid on auction {auction.get_id()} because the bid amount is less than the min bid amount"
            )
            return False
        print(f"user {bid.get_user().get_id()} is qualified to place bid on auction {auction.get_id()} based on the price criteria")
        return super().can_place_bid(auction, bid)
