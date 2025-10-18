from typing import TYPE_CHECKING
from app.factory.auction_decorator_factory import AuctionDecoratorFactory

if TYPE_CHECKING:
    from app.models.auction import Auction
    from app.models.bid import Bid
    from app.models.user import User


class AuctionStrategy:
    def __init__(self):
        self.decorator = AuctionDecoratorFactory.create_bid_place_checker_decorator()

    # Default implementation for each , should be overridden by the concrete strategies
    def determine_winner(self, auction: "Auction") -> "User":
        return next((bid.get_user() for bid in auction.get_bids() if bid.get_amount() == self.get_amount_to_settle_auction(auction)), None)

    def can_place_bid(self, auction: "Auction", bid: "Bid") -> bool:
        return self.decorator.can_place_bid(auction, bid)

    def get_amount_to_settle_auction(self, auction: "Auction") -> float:
        return auction.get_current_price()


class EnglishAuctionStrategy(AuctionStrategy):

    def can_place_bid(self, auction: "Auction", bid: "Bid") -> bool:
        return super().can_place_bid(auction, bid) and bid.get_amount() > auction.get_current_price()

    def get_amount_to_settle_auction(self, auction: "Auction") -> float:
        if not auction.get_bids():
            return auction.get_starting_price()
        # current price is the highest bid amount so we can safely return it
        return max(bid.get_amount() for bid in auction.get_bids())

    def determine_winner(self, auction: "Auction") -> "User":
        # Assuming there is only one winner
        return next((bid.get_user() for bid in auction.get_bids() if bid.get_amount() == self.get_amount_to_settle_auction(auction)), None)


class DutchAuctionStrategy(AuctionStrategy):
    def can_place_bid(self, auction: "Auction", bid: "Bid") -> bool:
        return super().can_place_bid(auction, bid) and bid.get_amount() < auction.get_current_price()

    def get_amount_to_settle_auction(self, auction: "Auction") -> float:
        if not auction.get_bids():
            return auction.get_starting_price()
        # Here also winner is the one who has placed the lowest bid
        return min(bid.get_amount() for bid in auction.get_bids())

    def determine_winner(self, auction: "Auction") -> "User":
        return next((bid.get_user() for bid in auction.get_bids() if bid.get_amount() == self.get_amount_to_settle_auction(auction)), None)


class SealedBidAuctionStrategy(AuctionStrategy):
    def can_place_bid(self, auction: "Auction", bid: "Bid") -> bool:
        return super().can_place_bid(auction, bid)

    def get_amount_to_settle_auction(self, auction: "Auction") -> float:
        if not auction.get_bids():
            return auction.get_starting_price()

        return max(bid.get_amount() for bid in auction.get_bids())

    def determine_winner(self, auction: "Auction") -> "User":
        return next((bid.get_user() for bid in auction.get_bids() if bid.get_amount() == self.get_amount_to_settle_auction(auction)), None)
