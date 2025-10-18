from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.mediator.auction_mediator import AuctionMediator


class AuctionComponent(ABC):
    def __init__(self):
        self._mediator = None

    def set_mediator(self, mediator: "AuctionMediator") -> None:
        self._mediator = mediator

    def get_mediator(self) -> "AuctionMediator":
        return self._mediator
