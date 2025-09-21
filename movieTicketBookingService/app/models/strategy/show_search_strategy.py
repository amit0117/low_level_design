from abc import ABC, abstractmethod
from app.models.show import Show
from datetime import datetime
from typing import Any
from app.models.enums import Genre


class ShowSearchStrategy(ABC):
    def __init__(self, shows: list[Show]):
        self.shows = shows

    @abstractmethod
    def search(self, query: Any) -> list[Show]:
        raise NotImplementedError("Subclasses must implement this method")


class DateTimeSearchStrategy(ShowSearchStrategy):
    def search(self, query: datetime) -> list[Show]:
        return [show for show in self.shows if query >= show.get_start_time() and query <= show.get_end_time()]


class MovieNameSearchStrategy(ShowSearchStrategy):
    def search(self, query: str) -> list[Show]:
        return [show for show in self.shows if query in show.movie.title]


class GenreSearchStrategy(ShowSearchStrategy):
    def search(self, query: Genre) -> list[Show]:
        return [show for show in self.shows if query in show.movie.genre]
