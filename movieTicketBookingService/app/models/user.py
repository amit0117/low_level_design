import uuid
from app.models.observer.movie_observer import MovieObserver
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.movie import Movie
    from app.models.booking import Booking


class User(MovieObserver):
    def __init__(self, name: str, email: str):
        self._id = uuid.uuid4()
        self.name = name
        self.email = email
        self.booking_history = []

    def update_movie_status(self, movie: "Movie"):
        print(f"User {self.name} received update for movie {movie.title}")

    def update_booking_status(self, booking: "Booking"):
        print(f"User {self.name} received update for booking {booking.id} and status is {booking.status}")

    @property
    def id(self):
        return self._id

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_booking_history(self):
        return self.booking_history

    def add_booking_to_history(self, booking: "Booking"):
        if booking in self.booking_history:
            print(f"Booking {booking.id} already in the booking history")
            return
        self.booking_history.append(booking)

    def remove_booking_from_history(self, booking: "Booking"):
        if booking not in self.booking_history:
            print(f"Booking {booking.id} not found in the booking history")
            return
        self.booking_history.remove(booking)
