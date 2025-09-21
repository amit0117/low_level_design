from app.models.movie import Movie
from app.models.seat import Seat
from app.models.screen import Screen
from datetime import datetime, timedelta
from app.models.strategy.show_pricing_strategy import ShowPricingStrategy
import uuid


class Show:
    def __init__(self, name: str, movie: Movie, screen: Screen, start_time: datetime, pricing_strategy: ShowPricingStrategy):
        self._id = str(uuid.uuid4())
        self._name = name
        self._movie = movie
        self._screen = screen
        self._start_time = start_time
        self._pricing_strategy = pricing_strategy

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def movie(self) -> Movie:
        return self._movie

    @property
    def screen(self) -> Screen:
        return self._screen

    @property
    def show_time(self) -> datetime:
        return self._start_time

    def get_movie(self) -> Movie:
        return self._movie

    def get_screen(self) -> Screen:
        return self._screen

    def get_start_time(self) -> datetime:
        return self._start_time

    def get_end_time(self) -> datetime:
        return self._start_time + timedelta(minutes=self._movie.get_duration())

    def get_pricing_strategy(self) -> ShowPricingStrategy:
        return self._pricing_strategy

    def set_pricing_strategy(self, pricing_strategy: ShowPricingStrategy) -> None:
        self._pricing_strategy = pricing_strategy
