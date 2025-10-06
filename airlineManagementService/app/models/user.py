from app.models.enums import UserType, PassengerType, StaffType
from uuid import uuid4
from app.observers.flight_observer import FlightObserver
from app.observers.booking_observer import BookingObserver
from app.models.flight import Flight
from app.models.booking import Booking


class User(FlightObserver, BookingObserver):
    def __init__(self, name: str, email: str, user_type: UserType):
        super().__init__()
        self.id = str(uuid4())
        self.name = name
        self.email = email
        self.user_type = user_type
        self.bookings: list[Booking] = []

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_email(self) -> str:
        return self.email

    def get_user_type(self) -> UserType:
        return self.user_type

    def update_flight_status(self, flight: Flight) -> None:
        print(f"User {self.name} notified about flight {flight.get_flight_number()} status change to {flight.get_status()}\n")

    def update_booking_status(self, booking: Booking) -> None:
        print(f"User {self.name} notified about booking {booking.get_booking_id()} status change to {booking.get_status()}\n")

    def add_booking_to_history(self, booking: Booking) -> None:
        self.bookings.append(booking)

class Passenger(User):
    def __init__(self, name: str, email: str, passenger_type: PassengerType):
        super().__init__(name, email, UserType.PASSENGER)
        self.passenger_type = passenger_type

    def get_passenger_type(self) -> PassengerType:
        return self.passenger_type


class Staff(User):
    def __init__(self, name: str, email: str, staff_type: StaffType):
        super().__init__(name, email, UserType.AIRLINE_STAFF)
        self.staff_type = staff_type

    def get_staff_type(self) -> StaffType:
        return self.staff_type


class Admin(User):
    def __init__(self, name: str, email: str):
        super().__init__(name, email, UserType.ADMIN)
