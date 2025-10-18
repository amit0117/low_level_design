# Considering 1-1 mapping between Auction and AuctionItem
from app.models.auction_item import AuctionItem
from app.models.bid import Bid
from app.models.enums import AuctionStatus, AuctionType
from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from app.observers.auction_observer import AuctionSubject
from uuid import uuid4
from app.state.auction_state import AuctionState, PendingAuctionState
from app.strategies.auction_strategy import AuctionStrategy, EnglishAuctionStrategy, DutchAuctionStrategy, SealedBidAuctionStrategy
from app.mediator.auction_component import AuctionComponent


if TYPE_CHECKING:
    from app.models.auction_item import AuctionItem
    from app.models.bid import Bid
    from app.models.user import User


class Auction(AuctionSubject, AuctionComponent):
    def __init__(
        self,
        owner: "User",
        item: "AuctionItem",
        start_time: datetime,
        end_time: datetime,
        starting_price: float = 0.0,
        auction_type: AuctionType = AuctionType.ENGLISH,
    ):
        AuctionSubject.__init__(self)
        AuctionComponent.__init__(self)
        self.id = str(uuid4())
        self.owner = owner
        self.item = item
        self.starting_price = starting_price
        self.current_price = starting_price
        self.start_time = start_time
        self.end_time = end_time
        self.bids: list[Bid] = []
        self.status = AuctionStatus.ACTIVE
        self.state: AuctionState = PendingAuctionState()
        self.auction_type: AuctionType = auction_type
        self.auction_strategy: AuctionStrategy = None

    def get_id(self) -> str:
        return self.id

    def get_owner(self) -> "User":
        return self.owner

    def get_item(self) -> "AuctionItem":
        return self.item

    def get_starting_price(self) -> float:
        return self.starting_price

    def get_current_price(self) -> float:
        return self.current_price

    def get_start_time(self) -> datetime:
        return self.start_time

    def get_end_time(self) -> datetime:
        return self.end_time

    def get_auction_duration(self) -> timedelta:
        return (self.end_time - self.start_time).total_seconds()

    def get_bids(self) -> list[Bid]:
        return self.bids.copy()

    def get_status(self) -> AuctionStatus:
        return self.status

    def get_auction_strategy(self) -> AuctionStrategy:
        return self.auction_strategy

    def start_auction(self) -> None:
        self.state.start_auction(self)

    def end_auction(self) -> None:
        self.state.end_auction(self)

    def cancel_auction(self) -> None:
        self.state.cancel_auction(self)

    def set_auction_strategy(self, auction_strategy: AuctionStrategy) -> None:
        self.auction_strategy = auction_strategy

    def set_state(self, state: AuctionState) -> None:
        self.state = state

    def set_status(self, status: AuctionStatus) -> None:
        self.status = status
        self.notify_observers_on_auction_status_change(self)

    def set_current_price(self, current_price: float) -> None:
        self.current_price = current_price

    def is_active(self) -> bool:
        return self.status == AuctionStatus.ACTIVE and datetime.now() <= self.end_time and datetime.now() >= self.start_time

    def get_amount_to_settle_auction(self) -> float:
        return self.auction_strategy.get_amount_to_settle_auction(self)

    def determine_winner(self) -> "User":
        return self.auction_strategy.determine_winner(self)

    def can_place_bid(self, bid: "Bid") -> bool:

        # Check if auction strategy allows this bid
        if not self.auction_strategy.can_place_bid(self, bid):
            print(f"Bid validation failed: strategy rejected bid for auction {self.get_id()}")
            return False

        return True

    def can_remove_bid(self, bid: "Bid") -> bool:
        """Check if the bid can be removed based on auction state"""
        return self.state.can_remove_bid(self, bid)

    def add_bid(self, bid: "Bid") -> None:
        """Add a bid to the auction"""
        self.bids.append(bid)

    def remove_bid(self, bid: "Bid") -> bool:
        """Remove a bid from this auction"""
        # Validate if bid can be removed
        if not self.can_remove_bid(bid):
            return False

        self.bids.remove(bid)

        new_price = self.auction_strategy.get_amount_to_settle_auction(self)
        self.set_current_price(new_price)

        bid.get_user().remove_from_bidding_history(bid)

        self.notify_observers_on_bid(bid, message=f"Bid {bid.get_id()} removed from auction {self.get_id()} by {bid.get_user().get_name()}")

        return True

    def place_bid(self, bid: "Bid") -> bool:
        if not self.can_place_bid(bid):
            return False

        # Add the bid
        self.add_bid(bid)

        # Update current price using strategy
        new_price = self.auction_strategy.get_amount_to_settle_auction(self)
        self.set_current_price(new_price)

        # Add user as observer if not already
        if not bid.get_user() in self.observers:
            self.add_observer(bid.get_user())

        # Update user's bidding history
        bid.get_user().add_to_bidding_history(bid)

        # Notify all observers about the new bid
        self.notify_observers_on_bid(bid)

        return True


class EnglishAuction(Auction):
    def __init__(self, owner: "User", item: "AuctionItem", start_time: datetime, end_time: datetime, starting_price: float = 0.0):
        super().__init__(owner, item, start_time, end_time, starting_price, AuctionType.ENGLISH)
        self.auction_strategy = EnglishAuctionStrategy()


class DutchAuction(Auction):
    def __init__(self, owner: "User", item: "AuctionItem", start_time: datetime, end_time: datetime, starting_price: float = 0.0):
        super().__init__(owner, item, start_time, end_time, starting_price, AuctionType.DUTCH)
        self.auction_strategy = DutchAuctionStrategy()


class SealedBidAuction(Auction):
    def __init__(self, owner: "User", item: "AuctionItem", start_time: datetime, end_time: datetime, starting_price: float = 0.0):
        super().__init__(owner, item, start_time, end_time, starting_price, AuctionType.SEALED_BID)
        self.auction_strategy = SealedBidAuctionStrategy()
