from app.strategies.search_strategy import AuctionSearchStrategy
from typing import Any, Optional
from app.models.auction import Auction


class SearchService:
    def __init__(self, search_strategy: Optional[AuctionSearchStrategy] = None):
        self.search_strategy = search_strategy

    def search(self, query: Any) -> list[Auction]:
        if not self.search_strategy:
            raise ValueError("Search strategy is not set")
        return self.search_strategy.search(query)

    def set_search_strategy(self, search_strategy: AuctionSearchStrategy) -> None:
        self.search_strategy = search_strategy

    def get_search_strategy(self) -> AuctionSearchStrategy:
        return self.search_strategy
