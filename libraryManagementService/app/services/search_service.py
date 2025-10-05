from app.strategies.item_search_strategy import ItemSearchStrategy
from app.models.library_item import LibraryItem


class SearchService:
    def __init__(self):
        self.search_strategy: ItemSearchStrategy = None

    def set_search_strategy(self, search_strategy: ItemSearchStrategy):
        self.search_strategy = search_strategy

    def search(self, query: str) -> list[LibraryItem]:
        if self.search_strategy is None:
            raise ValueError("Search strategy is not set")
        return self.search_strategy.search(query)
