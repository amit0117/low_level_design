from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from app.models.enums import AuctionStatus

if TYPE_CHECKING:
    from app.models.auction import Auction
    from app.models.bid import Bid


class AuctionState(ABC):
    @abstractmethod
    def start_auction(self, auction: "Auction") -> None:
        raise NotImplementedError("start_auction method has not been implemented")

    @abstractmethod
    def end_auction(self, auction: "Auction") -> None:
        raise NotImplementedError("end_auction method has not been implemented")

    @abstractmethod
    def cancel_auction(self, auction: "Auction") -> None:
        raise NotImplementedError("cancel_auction method has not been implemented")


class PendingAuctionState(AuctionState):
    def start_auction(self, auction: "Auction") -> None:
        print("Starting a pending auction...\n")
        auction.set_state(ActiveAuctionState())
        auction.set_status(AuctionStatus.ACTIVE)

    def end_auction(self, auction: "Auction") -> None:
        print("Cannot end a pending auction...\n")

    def cancel_auction(self, auction: "Auction") -> None:
        print("Cancelling a pending auction...\n")
        auction.set_status(AuctionStatus.CANCELLED)
        auction.set_state(CancelledAuctionState())


class ActiveAuctionState(AuctionState):
    def start_auction(self, auction: "Auction") -> None:
        print("Auction is already active...\n")

    def end_auction(self, auction: "Auction") -> None:
        print("Ending an active auction...\n")
        auction.set_status(AuctionStatus.CLOSED)
        auction.set_state(ClosedAuctionState())

    def cancel_auction(self, auction: "Auction") -> None:
        print("Cancelling an active auction...\n")
        auction.set_status(AuctionStatus.CANCELLED)
        auction.set_state(CancelledAuctionState())


class ClosedAuctionState(AuctionState):
    def start_auction(self, auction: "Auction") -> None:
        print("Starting a closed auction...\n")
        auction.set_state(ActiveAuctionState())
        auction.set_status(AuctionStatus.ACTIVE)

    def end_auction(self, auction: "Auction") -> None:
        print("Auction is already closed...\n")

    def cancel_auction(self, auction: "Auction") -> None:
        print("Cannot cancel a closed auction...\n")


class CancelledAuctionState(AuctionState):
    def start_auction(self, auction: "Auction") -> None:
        print("Cannot start a cancelled auction...\n")

    def end_auction(self, auction: "Auction") -> None:
        print("Cannot end a cancelled auction...\n")

    def cancel_auction(self, auction: "Auction") -> None:
        print("Auction is already cancelled...\n")
