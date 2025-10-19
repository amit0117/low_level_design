from app.chain.handler import AuctionChainBuilder
from app.models.user import User
from app.repositories.auction_repository import AuctionRepository
from app.repositories.user_repository import UserRepository
from app.services.payment_service import PaymentService
from app.mediator.auction_mediator import ConcreteAuctionMediator
from app.factory.auction_factory import EnglishAuctionFactory, DutchAuctionFactory, SealedBidAuctionFactory
from threading import Lock
from typing import Optional
from app.models.auction_item import AuctionItem
from datetime import datetime
from app.models.auction import Auction
from app.models.enums import AuctionType
from app.models.bid import Bid
from app.commands.auction_command import PlaceBidCommand


class OnlineAuctionSystem:
    _instance: Optional["OnlineAuctionSystem"] = None
    _lock: Lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._has_initialized = False
        return cls._instance

    def __init__(self):
        if self._has_initialized:
            return
        self._has_initialized = True
        self.auction_repository = AuctionRepository()
        self.user_repository = UserRepository()
        self.payment_service = PaymentService()
        self.auction_chain = AuctionChainBuilder.create_bid_processing_chain()
        self.mediator = ConcreteAuctionMediator()

        # Initialize auction factories
        self.english_factory = EnglishAuctionFactory()
        self.dutch_factory = DutchAuctionFactory()
        self.sealed_bid_factory = SealedBidAuctionFactory()

    def register_user(self, name: str, email: str, password: str) -> User:
        user = User(name, email, password)
        self.user_repository.add_user(user)
        self.mediator.register_component(user)
        return user

    def login_user(self, email: str, password: str) -> User:
        user = self.user_repository.get_user_by_email(email)
        if not user:
            print(f"User {email} not found")
            return None
        if not user.is_valid_password(password):
            print(f"Invalid password for user {user.get_name()}")
            return None
        print(f"User {user.get_name()} logged in successfully")
        return user

    def create_auction(
        self,
        user: User,
        item: AuctionItem,
        start_time: datetime,
        end_time: datetime,
        starting_price: float,
        auction_type: AuctionType,
    ) -> Auction:
        # Use factory pattern to create the appropriate auction type
        if auction_type == AuctionType.ENGLISH:
            auction = self.english_factory.create_auction(user, item, start_time, end_time, starting_price)
        elif auction_type == AuctionType.DUTCH:
            auction = self.dutch_factory.create_auction(user, item, start_time, end_time, starting_price)
        elif auction_type == AuctionType.SEALED_BID:
            auction = self.sealed_bid_factory.create_auction(user, item, start_time, end_time, starting_price)
        else:
            raise ValueError(f"Unsupported auction type: {auction_type}")

        self.auction_repository.add_auction(auction)
        self.mediator.register_component(auction)
        user.add_auction_to_history(auction)
        return auction

    def place_bid(self, bid: Bid) -> bool:
        # This will work as a invoker for the command pattern
        command = PlaceBidCommand(bid)
        return command.execute()

    def remove_bid(self, bid: Bid) -> bool:
        # This will work as a invoker for the command pattern
        command = PlaceBidCommand(bid)
        return command.undo()

    def start_auction(self, auction: Auction) -> None:
        auction.start_auction()

    def end_auction(self, auction: Auction) -> None:
        auction.end_auction()

    def cancel_auction(self, auction: Auction) -> None:
        auction.cancel_auction()
