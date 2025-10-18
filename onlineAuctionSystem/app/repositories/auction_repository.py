from threading import Lock
from app.models.user import User
from app.models.auction import Auction
from app.models.enums import AuctionStatus
from typing import Optional


class AuctionRepository:
    _instance: "AuctionRepository" = None
    _lock: Lock = Lock()

    def __new__(cls) -> "AuctionRepository":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "auctions"):
            return
        self.auctions: dict[str, Auction] = dict()

    @classmethod
    def get_instance(cls) -> "AuctionRepository":
        return cls._instance or cls()

    def add_auction(self, auction: Auction) -> None:
        with self._lock:
            self.auctions[auction.get_id()] = auction

    def get_auction(self, id: str) -> Auction:
        return self.auctions.get(id)

    def get_all_auctions(self) -> list[Auction]:
        return list(self.auctions.values())

    def remove_auction(self, id: str) -> None:
        with self._lock:
            self.auctions.pop(id, None)

    def get_auctions_by_user(self, user: User, status: Optional[AuctionStatus] = AuctionStatus.ACTIVE) -> list[Auction]:
        return [auction for auction in self.auctions.values() if auction.get_owner() == user and auction.get_status() == status]

    def start_auction(self, id: str) -> None:
        with self._lock:
            self.auctions[id].start_auction()

    def end_auction(self, id: str) -> None:
        with self._lock:
            self.auctions[id].end_auction()

    def cancel_auction(self, id: str) -> None:
        with self._lock:
            self.auctions[id].cancel_auction()