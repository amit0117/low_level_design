from app.models.show import Show
from app.models.movie import Movie
from app.models.enums import Genre
from typing import Any


class SearchService:
    def __init__(self) -> None:
        self.shows: list[Show] = []
        self.movies: list[Movie] = []

    def search_movies_by_name(self, name: str) -> list[Movie]:
        return [movie for movie in self.movies if name.lower() in movie.title.lower()]

    def search_movies_by_genre(self, genre: Genre) -> list[Movie]:
        return [movie for movie in self.movies if movie.genre == genre]

    def search_shows_by_city(self, city: str) -> list[Show]:
        return [show for show in self.shows if city.lower() in show.screen.cinema.city.lower()]

    def add_show(self, show: Show) -> None:
        if show not in self.shows:
            self.shows.append(show)

    def add_movie(self, movie: Movie) -> None:
        if movie not in self.movies:
            self.movies.append(movie)

    def remove_show(self, show: Show) -> None:
        if show in self.shows:
            self.shows.remove(show)
