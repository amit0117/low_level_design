from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.bid import Bid
    from app.models.auction import Auction
    from app.models.user import User


class AuctionComponent(ABC):

    def __init__(self):
        self._mediator = None

    def set_mediator(self, mediator: "AuctionMediator") -> None:
        self._mediator = mediator

    def get_mediator(self) -> "AuctionMediator":
        return self._mediator


class AuctionMediator(ABC):

    @abstractmethod
    def handle_bid_placement(self, bid: "Bid") -> bool:
        raise NotImplementedError("handle_bid_placement method has not been implemented")

    @abstractmethod
    def handle_bid_removal(self, bid: "Bid") -> bool:
        raise NotImplementedError("handle_bid_removal method has not been implemented")

    @abstractmethod
    def register_component(self, component: AuctionComponent) -> None:
        raise NotImplementedError("register_component method has not been implemented")


class ConcreteAuctionMediator(AuctionMediator):

    def __init__(self):
        self._components: dict[str, AuctionComponent] = {}
        self._auctions: dict[str, "Auction"] = {}
        self._users: dict[str, "User"] = {}

    def register_component(self, component: AuctionComponent) -> None:
        if hasattr(component, "get_id"):
            component_id = component.get_id()
            self._components[component_id] = component
            component.set_mediator(self)

            if isinstance(component, Auction):
                self._auctions[component_id] = component
            elif isinstance(component, User):
                self._users[component_id] = component

    def handle_bid_placement(self, bid: "Bid") -> bool:
        auction = bid.get_auction()
        if not auction:
            print("Mediator: Invalid bid - missing auction")
            return False

        return auction.place_bid(bid)

    def handle_bid_removal(self, bid: "Bid") -> bool:
        auction = bid.get_auction()
        if not auction:
            print("Mediator: Invalid bid - missing auction")
            return False

        return auction.remove_bid(bid)

    def get_auction(self, auction_id: str) -> "Auction":
        return self._auctions.get(auction_id)

    def get_user(self, user_id: str) -> "User":
        return self._users.get(user_id)
