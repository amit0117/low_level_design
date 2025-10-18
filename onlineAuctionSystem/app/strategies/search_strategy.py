from abc import ABC, abstractmethod
from app.models.auction import Auction
from app.repositories.auction_repository import AuctionRepository
from typing import Any
from datetime import datetime
from app.models.enums import AuctionStatus


class AuctionSearchStrategy(ABC):
    @abstractmethod
    def search(self, query: Any) -> list[Auction]:
        raise NotImplementedError("Subclasses must implement this method")


class AuctionItemTitleSearchStrategy(AuctionSearchStrategy):
    def __init__(self):
        self.auction_repository = AuctionRepository()

    def search(self, query: str) -> list[Auction]:
        return [auction for auction in self.auction_repository.get_all_auctions() if auction.get_item().get_name().lower() in query.lower()][:4]


class AuctionItemStartingPriceSearchStrategy(AuctionSearchStrategy):
    def __init__(self):
        self.auction_repository = AuctionRepository()

    def search(self, query: str) -> list[Auction]:
        return [auction for auction in self.auction_repository.get_all_auctions() if auction.get_item().get_starting_price() == float(query)][:4]


class AuctionItemStartingPriceRangeSearchStrategy(AuctionSearchStrategy):
    def __init__(self):
        self.auction_repository = AuctionRepository()

    def search(self, query: tuple[float, float]) -> list[Auction]:
        return [
            auction
            for auction in self.auction_repository.get_all_auctions()
            if auction.get_item().get_starting_price() >= query[0] and auction.get_item().get_starting_price() <= query[1]
        ][:4]


class AuctionDurationSearchStrategy(AuctionSearchStrategy):
    def __init__(self):
        self.auction_repository = AuctionRepository()

    def search(self, query: datetime) -> list[Auction]:
        return [auction for auction in self.auction_repository.get_all_auctions() if auction.get_start_time() <= query <= auction.get_end_time()][:4]


class AuctionStatusSearchStrategy(AuctionSearchStrategy):
    def __init__(self):
        self.auction_repository = AuctionRepository()

    def search(self, query: AuctionStatus) -> list[Auction]:
        return [auction for auction in self.auction_repository.get_all_auctions() if auction.get_status() == query][:4]
