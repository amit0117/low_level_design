from abc import ABC, abstractmethod
from app.chain.handler import AuctionChainBuilder, AuctionRequest
from app.models.bid import Bid
from app.models.auction import Auction
from app.models.user import User
from app.mediator.auction_component import AuctionComponent


class AuctionMediator(ABC):

    @abstractmethod
    def handle_bid_placement(self, bid: Bid) -> bool:
        raise NotImplementedError("handle_bid_placement method has not been implemented")

    @abstractmethod
    def handle_bid_removal(self, bid: Bid) -> bool:
        raise NotImplementedError("handle_bid_removal method has not been implemented")

    @abstractmethod
    def register_component(self, component: AuctionComponent) -> None:
        raise NotImplementedError("register_component method has not been implemented")


class ConcreteAuctionMediator(AuctionMediator):

    def __init__(self):
        self._components: dict[str, AuctionComponent] = {}
        self._auctions: dict[str, Auction] = {}
        self._users: dict[str, User] = {}
        self.bid_processing_chain = AuctionChainBuilder.create_bid_processing_chain()

    def register_component(self, component: AuctionComponent) -> None:
        if hasattr(component, "get_id"):
            component_id = component.get_id()
            self._components[component_id] = component
            component.set_mediator(self)

            if isinstance(component, Auction):
                self._auctions[component_id] = component
            elif isinstance(component, User):
                self._users[component_id] = component

    def handle_bid_placement(self, bid: Bid) -> bool:
        auction = bid.get_auction()
        user = bid.get_user()

        if not auction or not user:
            print("Mediator: Invalid bid - missing auction or user")
            return False

        request = AuctionRequest(bid, user, "place_bid")

        if not self.bid_processing_chain.handle(request):
            print("Mediator: Chain processing failed for bid placement")
            return False

        print(f"Mediator: Chain processing passed, delegating to auction {auction.get_id()}")
        return auction.place_bid(bid)

    def handle_bid_removal(self, bid: Bid) -> bool:
        auction = bid.get_auction()
        if not auction:
            print("Mediator: Invalid bid - missing auction")
            return False

        return auction.remove_bid(bid)

    def get_auction(self, auction_id: str) -> Auction:
        return self._auctions.get(auction_id)

    def get_user(self, user_id: str) -> User:
        return self._users.get(user_id)
