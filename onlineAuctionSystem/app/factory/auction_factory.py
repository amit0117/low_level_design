from app.models.auction import Auction
from app.models.user import User
from app.models.auction_item import AuctionItem
from app.models.enums import AuctionType
from abc import ABC, abstractmethod
from datetime import datetime
from app.models.auction import EnglishAuction, DutchAuction, SealedBidAuction


class AuctionFactory(ABC):
    @abstractmethod
    def create_auction(
        self, owner: User, item: AuctionItem, start_time: datetime, end_time: datetime, auction_type: AuctionType, starting_price: float = 0.0
    ) -> Auction:
        raise NotImplementedError("create_auction method has not been implemented")


class EnglishAuctionFactory(AuctionFactory):
    def create_auction(
        self, owner: "User", item: "AuctionItem", start_time: datetime, end_time: datetime, starting_price: float = 0.0
    ) -> "EnglishAuction":
        return EnglishAuction(owner, item, start_time, end_time, starting_price)


class DutchAuctionFactory(AuctionFactory):
    def create_auction(
        self, owner: "User", item: "AuctionItem", start_time: datetime, end_time: datetime, starting_price: float = 0.0
    ) -> "DutchAuction":
        return DutchAuction(owner, item, start_time, end_time, starting_price)


class SealedBidAuctionFactory(AuctionFactory):
    def create_auction(
        self, owner: "User", item: "AuctionItem", start_time: datetime, end_time: datetime, starting_price: float = 0.0
    ) -> "SealedBidAuction":
        return SealedBidAuction(owner, item, start_time, end_time, starting_price)
