"""
Airline Management System Facade

This module provides a singleton facade for the Airline Management System,
handling all major operations including user management, flight operations,
booking management, and aircraft operations.

Design Patterns Applied:
- Singleton Pattern: Ensures only one instance of the facade exists
- Facade Pattern: Provides a simplified interface to complex subsystems
- Repository Pattern: Uses repositories for data access
- Service Pattern: Uses services for business logic

Author: Amit Kumar
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from threading import Lock

# Import models
from app.models.user import User, Passenger, Staff, Admin
from app.models.flight import Flight
from app.models.aircraft import Aircraft
from app.models.booking import Booking
from app.models.seat import Seat

# Import enums
from app.models.enums import UserType, PassengerType, StaffType, FlightStatus, BookingStatus, SeatType, SeatStatus, PaymentMethod

# Import repositories
from app.repositories.user_repository import UserRepository
from app.repositories.flight_repository import FlightRepository
from app.repositories.booking_repository import BookingRepository

# Import services
from app.services.booking_service import BookingService
from app.services.payment_service import PaymentService

# Import strategies
from app.strategies.payment_strategy import PaymentStrategy


class AirlineManagementFacade:
    """
    Singleton Facade for Airline Management System

    This facade provides a unified interface for all airline operations
    including user management, flight operations, booking management,
    and aircraft operations.
    """

    _instance: Optional["AirlineManagementFacade"] = None
    _lock: Lock = Lock()

    def __new__(cls) -> "AirlineManagementFacade":
        """Singleton implementation with thread safety"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the facade with all required repositories and services"""
        if hasattr(self, "_initialized"):
            return

        # Initialize repositories
        self._user_repository = UserRepository.get_instance()
        self._flight_repository = FlightRepository.get_instance()
        self._booking_repository = BookingRepository.get_instance()

        # Initialize services
        self._booking_service = BookingService()
        self._payment_service = PaymentService()

        self._initialized = True

    @classmethod
    def get_instance(cls) -> "AirlineManagementFacade":
        """Get the singleton instance of the facade"""
        return cls._instance or cls()

    # ==================== USER MANAGEMENT OPERATIONS ====================

    def create_passenger(self, name: str, email: str, passenger_type: PassengerType) -> Passenger:
        """Create a new passenger"""
        passenger = Passenger(name, email, passenger_type)
        self._user_repository.add_user(passenger)
        return passenger

    def create_staff(self, name: str, email: str, staff_type: StaffType) -> Staff:
        """Create a new airline staff member"""
        staff = Staff(name, email, staff_type)
        self._user_repository.add_user(staff)
        return staff

    def create_admin(self, name: str, email: str) -> Admin:
        """Create a new admin user"""
        admin = Admin(name, email)
        self._user_repository.add_user(admin)
        return admin

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self._user_repository.get_user(user_id)

    def get_all_users(self) -> List[User]:
        """Get all users"""
        return self._user_repository.get_all_users()

    def get_all_passengers(self) -> List[Passenger]:
        """Get all passengers"""
        return self._user_repository.get_all_passengers()

    def get_all_staff(self) -> List[Staff]:
        """Get all airline staff"""
        return self._user_repository.get_all_airline_staff()

    def get_all_admins(self) -> List[Admin]:
        """Get all admin users"""
        return self._user_repository.get_all_admins()

    def get_users_by_type(self, user_type: UserType) -> List[User]:
        """Get users by type"""
        return self._user_repository.get_all_users_by_type(user_type)

    def update_user(self, user_id: str, updated_user: User) -> bool:
        """Update user information"""
        try:
            self._user_repository.update_user(user_id, updated_user)
            return True
        except Exception:
            return False

    def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        try:
            self._user_repository.delete_user(user_id)
            return True
        except Exception:
            return False

    # ==================== AIRCRAFT MANAGEMENT OPERATIONS ====================

    def create_aircraft(self, model: str, total_seats: int, tail_number: str) -> Aircraft:
        """Create a new aircraft"""
        aircraft = Aircraft(model, total_seats, tail_number)
        return aircraft

    # ==================== FLIGHT MANAGEMENT OPERATIONS ====================

    def create_flight(
        self, flight_number: str, aircraft: Aircraft, source: str, destination: str, departure_time: datetime, arrival_time: datetime
    ) -> Flight:
        """Create a new flight"""
        flight = Flight(flight_number, aircraft, source, destination, departure_time, arrival_time)
        self._flight_repository.add_flight(flight)
        return flight

    def get_flight(self, flight_number: str) -> Optional[Flight]:
        """Get flight by flight number"""
        return self._flight_repository.get_flight_by_number(flight_number)

    def get_all_flights(self) -> List[Flight]:
        """Get all flights"""
        return self._flight_repository.get_all_flights()

    def get_flights_by_status(self, status: FlightStatus) -> List[Flight]:
        """Get flights by status"""
        return self._flight_repository.get_all_flights_by_status(status)

    def get_flights_by_route(self, source: str, destination: str) -> List[Flight]:
        """Get flights by route"""
        return self._flight_repository.get_all_flights_between_source_and_destination(source, destination)

    def get_flights_by_date_range(self, source: str, destination: str, start_date: datetime, end_date: datetime) -> List[Flight]:
        """Get flights by date range"""
        return self._flight_repository.get_all_flights_between_source_and_destination_within_a_date_range(source, destination, start_date, end_date)

    def update_flight_status(self, flight_number: str, status: FlightStatus) -> bool:
        """Update flight status"""
        try:
            flight = self._flight_repository.get_flight_by_number(flight_number)
            if flight:
                flight.set_status(status)
                return True
            return False
        except Exception:
            return False

    def add_seat_to_flight(self, flight_number: str, seat: Seat) -> bool:
        """Add seat to flight"""
        try:
            flight = self._flight_repository.get_flight_by_number(flight_number)
            if flight:
                flight.add_seat(seat)
                return True
            return False
        except Exception:
            return False

    def get_available_seats(self, flight_number: str) -> List[Seat]:
        """Get available seats for a flight"""
        flight = self._flight_repository.get_flight_by_number(flight_number)
        if flight:
            return flight.get_available_seats()
        return []

    def get_flight_seats(self, flight_number: str) -> Dict[int, Seat]:
        """Get all seats for a flight"""
        flight = self._flight_repository.get_flight_by_number(flight_number)
        if flight:
            return flight.get_all_seats()
        return {}

    # ==================== BOOKING MANAGEMENT OPERATIONS ====================

    def search_and_lock_seats(
        self,
        source: str,
        destination: str,
        total_seats_required: int,
        seat_type: SeatType,
        passenger: Passenger,
        start_date: datetime,
        end_date: datetime,
    ) -> tuple[Flight, List[Seat]]:
        """Search flights and lock seats for booking"""
        return self._booking_service.lock_seats_for_booking(source, destination, total_seats_required, seat_type, passenger, start_date, end_date)

    def create_booking(
        self, flight: Flight, passenger: Passenger, seats: List[Seat], payment_strategy: PaymentStrategy, total_amount: float
    ) -> Booking:
        """Create a new booking"""
        return self._booking_service.create_booking(flight, passenger, seats, payment_strategy, total_amount)

    def get_booking(self, booking_id: str) -> Optional[Booking]:
        """Get booking by ID"""
        return self._booking_repository.get_booking(booking_id)

    def get_all_bookings(self) -> List[Booking]:
        """Get all bookings"""
        return self._booking_repository.get_all_bookings()

    def get_bookings_by_passenger(self, passenger: Passenger) -> List[Booking]:
        """Get bookings by passenger"""
        return self._booking_repository.get_all_bookings_by_passenger(passenger)

    def get_bookings_by_flight(self, flight: Flight) -> List[Booking]:
        """Get bookings by flight"""
        return self._booking_repository.get_all_bookings_by_flight(flight)

    def get_bookings_by_status(self, status: BookingStatus) -> List[Booking]:
        """Get bookings by status"""
        return self._booking_repository.get_all_bookings_by_status(status)

    def get_bookings_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Booking]:
        """Get bookings by date range"""
        return self._booking_repository.get_all_bookings_by_date_range(start_date, end_date)

    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel a booking"""
        try:
            self._booking_service.cancel_booking(booking_id)
            return True
        except Exception:
            return False

    def board_passenger(self, booking_id: str) -> bool:
        """Board a passenger"""
        try:
            self._booking_service.boarding_passenger(booking_id)
            return True
        except Exception:
            return False

    def complete_flight(self, flight_number: str) -> bool:
        """Complete a flight and release all seats"""
        try:
            self._booking_service.complete_a_flight(flight_number)
            return True
        except Exception:
            return False

    # ==================== PAYMENT OPERATIONS ====================

    def process_payment(self, payment_strategy: PaymentStrategy, amount: float) -> Any:
        """Process payment using specified strategy"""
        self._payment_service.set_payment_strategy(payment_strategy)
        return self._payment_service.process_payment(amount)

    # ==================== SEAT MANAGEMENT OPERATIONS ====================

    def lock_seats(self, flight_number: str, seats: List[Seat], passenger: Passenger) -> bool:
        """Lock seats for a passenger"""
        try:
            flight = self._flight_repository.get_flight_by_number(flight_number)
            if flight:
                return flight.lock_seats(seats, passenger)
            return False
        except Exception:
            return False

    def release_seats(self, flight_number: str, seats: List[Seat], passenger: Passenger) -> bool:
        """Release locked seats"""
        try:
            flight = self._flight_repository.get_flight_by_number(flight_number)
            if flight:
                flight.release_seats(seats, passenger)
                return True
            return False
        except Exception:
            return False

    def get_locked_seats_by_passenger(self, flight_number: str, passenger: Passenger) -> List[Seat]:
        """Get locked seats by passenger"""
        flight = self._flight_repository.get_flight_by_number(flight_number)
        if flight:
            return flight.get_locked_seats_by_passenger(passenger)
        return []

    # ==================== SEARCH AND FILTERING OPERATIONS ====================

    def search_flights(
        self, source: str, destination: str, departure_date: datetime, seat_type: Optional[SeatType] = None, max_price: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Search flights with filters"""
        flights = self._flight_repository.get_all_flights_between_source_and_destination(source, destination)

        # Filter by departure date
        flights = [f for f in flights if f.get_departure_time().date() == departure_date.date()]

        results = []
        for flight in flights:
            available_seats = flight.get_available_seats()

            # Filter by seat type if specified
            if seat_type:
                available_seats = [seat for seat in available_seats if seat.get_seat_type() == seat_type]

            # Filter by max price if specified
            if max_price:
                available_seats = [seat for seat in available_seats if seat.get_price() <= max_price]

            if available_seats:
                result = {
                    "flight": flight,
                    "available_seats": available_seats,
                    "total_available_seats": len(available_seats),
                    "min_price": min(seat.get_price() for seat in available_seats),
                    "max_price": max(seat.get_price() for seat in available_seats),
                }
                results.append(result)

        return results

    def get_flight_statistics(self) -> Dict[str, Any]:
        """Get flight statistics"""
        all_flights = self._flight_repository.get_all_flights()
        all_bookings = self._booking_repository.get_all_bookings()

        stats = {
            "total_flights": len(all_flights),
            "total_bookings": len(all_bookings),
            "flights_by_status": {},
            "bookings_by_status": {},
            "total_revenue": sum(booking.get_price() for booking in all_bookings if booking.get_status() == BookingStatus.CONFIRMED),
        }

        # Count flights by status
        for status in FlightStatus:
            stats["flights_by_status"][status.value] = len([f for f in all_flights if f.get_status() == status])

        # Count bookings by status
        for status in BookingStatus:
            stats["bookings_by_status"][status.value] = len([b for b in all_bookings if b.get_status() == status])

        return stats

    def get_user_statistics(self) -> Dict[str, Any]:
        """Get user statistics"""
        all_users = self._user_repository.get_all_users()

        stats = {"total_users": len(all_users), "users_by_type": {}, "passengers_by_type": {}, "staff_by_type": {}}

        # Count users by type
        for user_type in UserType:
            stats["users_by_type"][user_type.value] = len([u for u in all_users if u.get_user_type() == user_type])

        # Count passengers by type
        passengers = self._user_repository.get_all_passengers()
        for passenger_type in PassengerType:
            stats["passengers_by_type"][passenger_type.value] = len([p for p in passengers if p.get_passenger_type() == passenger_type])

        # Count staff by type
        staff = self._user_repository.get_all_airline_staff()
        for staff_type in StaffType:
            stats["staff_by_type"][staff_type.value] = len([s for s in staff if s.get_staff_type() == staff_type])

        return stats
