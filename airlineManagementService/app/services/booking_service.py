from app.models.booking import Booking
from app.models.flight import Flight
from app.models.user import Passenger
from app.models.seat import Seat
from app.strategies.payment_strategy import PaymentStrategy
from app.repositories.booking_repository import BookingRepository
from app.repositories.flight_repository import FlightRepository
from app.repositories.user_repository import UserRepository
from app.services.payment_service import PaymentService
from app.models.enums import PaymentStatus, SeatStatus, SeatType
from datetime import datetime


class BookingService:
    def __init__(self) -> None:
        self.booking_repository = BookingRepository()
        self.flight_repository = FlightRepository()
        self.user_repository = UserRepository()
        self.payment_service = PaymentService()

    def lock_seats_for_booking(
        self,
        source: str,
        destination: str,
        total_seat_required: int,
        seat_type: SeatType,
        passenger: Passenger,
        start_date: datetime,
        end_date: datetime,
    ) -> tuple[Flight, list[Seat]]:
        flights = self.flight_repository.get_all_flights_between_source_and_destination_within_a_date_range(source, destination, start_date, end_date)
        if not flights:
            raise ValueError(f"No flights found between {source} and {destination} within the date range {start_date} and {end_date}")

        # try to check if the seats are available on any of the flights
        for flight in flights:
            available_seats = [seat for seat in flight.get_available_seats() if seat.get_seat_type() == seat_type]
            if len(available_seats) >= total_seat_required:
                seats = available_seats[:total_seat_required]
                print(
                    f"Found {len(seats)} seats for {passenger.get_name()} on flight {flight.get_flight_number()}, seats: [{", ".join([seat.get_seat_number() for seat in seats])}]"
                )
                # check if the seats can be locked
                if flight.lock_seats(seats, passenger):
                    return flight, seats

        raise ValueError(
            f"Seats cannot be locked on any of the flights between {source} and {destination} within the date range {start_date} and {end_date}"
        )

    def create_booking(
        self, flight: Flight, passenger: Passenger, seats: list[Seat], payment_strategy: PaymentStrategy, total_amount: float
    ) -> Booking:  # first pay for the booking
        # Check if the seats can be locked
        if not flight.lock_seats(seats, passenger):
            raise ValueError("Seats cannot be locked")

        self.payment_service.set_payment_strategy(payment_strategy)
        payment_result = self.payment_service.process_payment(total_amount)

        if payment_result.get_payment_status() != PaymentStatus.SUCCESS:
            raise ValueError("Payment failed")
        # assuming that the seats are already locked
        booking = Booking(flight, passenger, seats, payment_result)
        self.booking_repository.add_booking(booking)
        # Reserve the seats
        flight.book_seats(seats, passenger)
        # add to the booking history of the passenger
        passenger.add_booking_to_history(booking)
        return booking

    def boarding_passenger(self, booking_id: str) -> None:
        booking = self.booking_repository.get_booking(booking_id)
        if booking is None:
            raise ValueError("Booking not found")
        seats = booking.get_seats()
        # Change the status of the seats to BOARDING
        print(f"Boarding passenger {booking.get_passenger().get_name()} for booking {booking_id}")
        for seat in seats:
            seat.set_status(SeatStatus.OCCUPIED)
            seat.release_seat()

    def cancel_booking(self, booking_id: str) -> None:
        booking = self.booking_repository.get_booking(booking_id)
        if booking is None:
            raise ValueError("Booking not found")
        booking.cancel()

    def complete_a_flight(self, flight_number: str) -> None:
        flight = self.flight_repository.get_flight_by_number(flight_number)
        if flight is None:
            raise ValueError("Flight not found")

        # release the seats
        for seat in flight.get_all_seats().values():
            seat.release_seat()
