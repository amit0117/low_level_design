from app.commands.base_command import BaseCommand
from app.models.enums import ActionType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.auction import Auction
    from app.models.bid import Bid


class PlaceBidCommand(BaseCommand):
    def __init__(self, bid: "Bid"):
        self.bid = bid

    def execute(self) -> bool:
        """Execute the place bid command through mediator"""
        auction = self.bid.get_auction()
        mediator = auction.get_mediator()
        if not mediator:
            print(f"No mediator found for auction {auction.get_id()}")
            return False
        return mediator.handle_bid_placement(self.bid)

    def undo(self) -> bool:
        """Undo the place bid command through mediator"""
        auction = self.bid.get_auction()
        mediator = auction.get_mediator()
        if not mediator:
            print(f"No mediator found for auction {auction.get_id()}")
            return False
        return mediator.handle_bid_removal(self.bid)
