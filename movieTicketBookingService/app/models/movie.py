from app.models.observer.movie_observer import MovieSubject
from uuid import uuid4
from app.models.enums import Genre


class Movie(MovieSubject):
    def __init__(self, title: str, genre: Genre, duration_in_minutes: int):
        super().__init__()
        self._id = str(uuid4())
        self._title = title
        self._genre = genre
        self._duration_in_minutes = duration_in_minutes

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def genre(self) -> Genre:
        return self._genre

    def get_duration(self) -> int:
        return self._duration_in_minutes

    def release_movie(self) -> None:
        self.notify_observers(self)
