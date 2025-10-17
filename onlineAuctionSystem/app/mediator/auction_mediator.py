from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.bid import Bid


class Mediator(ABC):
    @abstractmethod
    def notify_mediator(self, args: Any, kwargs: Any) -> None:
        raise NotImplementedError("notify method has not been implemented")


class AuctionMediator(Mediator):
    # In our case Auction will act as a mediator between the users and the auction system
    # Since it has already list of bidders(who are also components for the mediators, So not initiating here)
    def notify_mediator(self, bid: "Bid") -> None:
        # Observer works great if:

        # You only want to notify all bidders whenever a new bid arrives.

        # No complex decision-making is required (just broadcast updates).

        # Mediator is better if:

        # You need rules and coordination:
        # e.g., check if bid > previous bid,
        # update auction state,
        # prevent bids after close,
        # notify only valid bidders,

        #  Use Observer pattern is better if:
        # Announce to everyone that the price changed.

        # Use Mediator pattern is better if:
        # Decide who wins, when bidding ends, and who to notify.

        # Notify all observers about the new bid
        self.notify_observers_on_bid(bid)
