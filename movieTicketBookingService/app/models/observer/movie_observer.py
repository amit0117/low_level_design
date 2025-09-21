from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.movie import Movie


class MovieObserver(ABC):
    @abstractmethod
    def update_movie_status(self, movie: "Movie"):
        raise NotImplementedError("Subclass must implement this method")


class MovieSubject:
    def __init__(self):
        self.observers: list[MovieObserver] = []

    def add_observer(self, observer: MovieObserver):
        self.observers.append(observer)

    def remove_observer(self, observer: MovieObserver):
        self.observers.remove(observer)

    def notify_observers(self, movie: "Movie"):
        for observer in self.observers:
            observer.update_movie_status(movie)
