from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.auction import Auction
    from app.models.bid import Bid


class AuctionValidator(ABC):
    @abstractmethod
    def can_place_bid(self, auction: "Auction", bid: "Bid") -> bool:
        raise NotImplementedError("can_place_bid method has not been implemented")


class ConcreteAuctionValidator(AuctionValidator):
    def can_place_bid(self, auction: "Auction", bid: "Bid") -> bool:
        if bid.get_auction() != auction or not auction.is_active():
            return False
        return True


class AuctionValidatorDecorator(AuctionValidator):
    def __init__(self, validator: AuctionValidator):
        self.validator = validator

    def can_place_bid(self, auction: "Auction", bid: "Bid") -> bool:
        return self.validator.can_place_bid(auction, bid)


class OwnerCheckDecorator(AuctionValidatorDecorator):
    def can_place_bid(self, auction: "Auction", bid: "Bid") -> bool:
        if bid.get_user().get_id() == auction.get_owner().get_id():
            print(f"OwnerCheckDecorator: User {bid.get_user().get_name()} cannot place bid on auction {auction.get_id()} because they are the owner")
            return False

        return super().can_place_bid(auction, bid)


class FraudDetectionDecorator(AuctionValidatorDecorator):
    def __init__(self, validator: AuctionValidator, max_bid_amount: float = 1000000, min_bid_amount: float = 100):
        super().__init__(validator)
        self.max_bid_amount = max_bid_amount
        self.min_bid_amount = min_bid_amount

    def can_place_bid(self, auction: "Auction", bid: "Bid") -> bool:
        if bid.get_amount() > self.max_bid_amount:
            print(
                f"FraudDetector: User {bid.get_user().get_name()} cannot place bid on auction {auction.get_id()} because the bid amount (₹{bid.get_amount()}) is greater than the max bid amount (₹{self.max_bid_amount})"
            )
            return False
        if bid.get_amount() < self.min_bid_amount:
            print(
                f"FraudDetector: User {bid.get_user().get_name()} cannot place bid on auction {auction.get_id()} because the bid amount (₹{bid.get_amount()}) is less than the min bid amount (₹{self.min_bid_amount})"
            )
            return False

        print(f"FraudDetector: User {bid.get_user().get_name()} is qualified to place bid on auction {auction.get_id()} based on the price criteria")

        return super().can_place_bid(auction, bid)
