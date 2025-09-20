from app.models.product import Product
from app.models.search_strategy import SearchStrategy
from typing import Optional


class SearchService:
    """Service for searching products"""

    def __init__(self, search_strategy: Optional[SearchStrategy] = None):
        self.search_strategy = search_strategy

    def search(self, query: str) -> list[Product]:
        if self.search_strategy is None:
            raise ValueError("Search strategy not set")
        return self.search_strategy.search(query)

    def set_strategy(self, strategy: SearchStrategy):
        self.search_strategy = strategy
