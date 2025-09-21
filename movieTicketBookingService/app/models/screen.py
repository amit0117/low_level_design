from app.models.seat import Seat
import uuid


class Screen:
    def __init__(self, name: str, seats: list[Seat] = []):
        self._id = str(uuid.uuid4())
        self._name = name
        self._seats = seats
        self._cinema = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def seats(self) -> list[Seat]:
        return self._seats

    @property
    def cinema(self):
        return self._cinema

    @cinema.setter
    def cinema(self, cinema):
        self._cinema = cinema

    def get_seats(self) -> list[Seat]:
        return self._seats

    def add_seat(self, seat: Seat) -> None:
        self._seats.append(seat)
