from app.services.payment_service import PaymentService
from app.services.search_service import SearchService
from app.services.booking_service import BookingService
from app.services.user_service import UserService
from app.models.user import User
from app.models.show import Show
from app.models.seat import Seat
from app.models.booking import Booking
from app.models.strategy.payment_strategy import PaymentStrategy
from typing import Optional
from threading import Lock
from app.models.cinema import Cinema
from app.models.movie import Movie
from app.models.enums import PaymentStatus


class MovieTicketBookingService:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "initialized", False):
            return
        self.payment_service = PaymentService()
        self.search_service = SearchService()
        self.booking_service = BookingService()
        self.user_service = UserService()
        self.cinema: dict[str, Cinema] = {}
        self.show: dict[str, Show] = {}
        self.movie: dict[str, Movie] = {}
        self.initialized = True

    @classmethod
    def get_instance(cls) -> "MovieTicketBookingService":
        return cls()

    def add_user(self, user: User) -> None:
        self.user_service.register_user(user)

    def get_user(self, user_id: str) -> User:
        if user_id not in self.user_service.users:
            raise ValueError(f"User with id {user_id} does not exist")
        return self.user_service.get_user(user_id)

    def add_show(self, show: Show) -> None:
        if show.id in self.show:
            raise ValueError(f"Show with id {show.id} already exists")
        self.show[show.id] = show

    def get_show(self, show_id: str) -> Show:
        if show_id not in self.show:
            raise ValueError(f"Show with id {show_id} does not exist")
        return self.show[show_id]

    def add_cinema(self, cinema: Cinema) -> None:
        if cinema.id in self.cinema:
            raise ValueError(f"Cinema with id {cinema.id} already exists")
        self.cinema[cinema.id] = cinema

    def get_cinema(self, cinema_id: str) -> Cinema:
        if cinema_id not in self.cinema:
            raise ValueError(f"Cinema with id {cinema_id} does not exist")
        return self.cinema[cinema_id]

    def add_movie(self, movie: Movie) -> None:
        if movie.id in self.movie:
            raise ValueError(f"Movie with id {movie.id} already exists")
        self.movie[movie.id] = movie

    def get_movie(self, movie_id: str) -> Movie:
        if movie_id not in self.movie:
            raise ValueError(f"Movie with id {movie_id} does not exist")
        return self.movie[movie_id]

    def book_tickets(self, user: User, show: Show, seats: list[Seat], payment_strategy: PaymentStrategy) -> Optional[Booking]:
        # Create booking
        booking = self.booking_service.create_booking(user, show, seats, payment_strategy)
        if booking is None:
            print("Booking failed. Please try again.")
            return None
        print(f"Booking {booking.id} created successfully.")

        # Process payment
        payment_result = self.payment_service.process_payment(booking.total_price, payment_strategy)
        if not payment_result.status == PaymentStatus.SUCCESS:
            print("Payment failed. Please try again.")
            return None

        print(f"Payment {payment_result.id} processed successfully.")
        # Confirm booking
        self.booking_service.confirm_booking(booking)
        return booking

    def cancel_booking(self, booking: Booking) -> None:
        self.booking_service.cancel_booking(booking)
