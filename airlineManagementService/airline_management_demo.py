"""
Airline Management System Demo

Comprehensive demonstration of the airline management system showcasing:
- User management (passengers, staff, admin)
- Flight creation and management
- Seat booking workflow (search, lock, reserve, occupy)
- Payment processing with price decorators
- Flight completion and statistics

Author: Amit Kumar
"""

from datetime import datetime, timedelta
from airline_management import AirlineManagementFacade
from app.models.enums import UserType, PassengerType, StaffType, FlightStatus, BookingStatus, SeatType, SeatStatus, PaymentMethod
from app.models.seat import Seat
from app.strategies.payment_strategy import CreditCardPaymentStrategy, DebitCardPaymentStrategy, CashPaymentStrategy, BankTransferPaymentStrategy
from app.decorators.booking_price_decorator import (
    BaseBookingPrice,
    TaxDecorator,
    ServiceChargeDecorator,
    BaggageFeeDecorator,
    DiscountDecorator,
    AirPortFeeDecorator,
)


def main():
    print("=== AIRLINE MANAGEMENT SYSTEM DEMO ===\n")

    # Get facade instance
    facade = AirlineManagementFacade.get_instance()

    # ==================== USER MANAGEMENT DEMO ====================
    print("1. CREATING USERS")
    print("-" * 30)

    # Create passengers
    passenger1 = facade.create_passenger("Rajesh Kumar", "rajesh@email.com", PassengerType.REGULAR)
    passenger2 = facade.create_passenger("Priya Sharma", "priya@email.com", PassengerType.FREQUENT_FLYER)
    passenger3 = facade.create_passenger("Amit Singh", "amit@email.com", PassengerType.CORPORATE)

    # Create staff
    pilot = facade.create_staff("Captain Vikram", "vikram@airline.com", StaffType.COCKPIT_CREW)
    attendant = facade.create_staff("Anita Patel", "anita@airline.com", StaffType.CABIN_CREW)
    ground_staff = facade.create_staff("Ravi Gupta", "ravi@airline.com", StaffType.GROUND_STAFF)

    # Create admin
    admin = facade.create_admin("Admin Manager", "admin@airline.com")

    print(f"Created {len(facade.get_all_users())} users")
    print(f"Passengers: {len(facade.get_all_passengers())}")
    print(f"Staff: {len(facade.get_all_staff())}")
    print(f"Admins: {len(facade.get_all_admins())}\n")

    # ==================== AIRCRAFT AND FLIGHT CREATION ====================
    print("2. CREATING AIRCRAFT AND FLIGHTS")
    print("-" * 40)

    # Create aircraft
    aircraft1 = facade.create_aircraft("Boeing 737", 150, "VT-ABC")
    aircraft2 = facade.create_aircraft("Airbus A320", 180, "VT-XYZ")

    # Create flights
    departure_time = datetime.now() + timedelta(days=1, hours=2)
    arrival_time = departure_time + timedelta(hours=3)

    # Create a wider date range for booking
    booking_start_date = departure_time - timedelta(hours=1)
    booking_end_date = arrival_time + timedelta(hours=1)

    flight1 = facade.create_flight("AI-101", aircraft1, "Delhi", "Mumbai", departure_time, arrival_time)

    flight2 = facade.create_flight("AI-102", aircraft2, "Mumbai", "Bangalore", departure_time + timedelta(hours=4), arrival_time + timedelta(hours=4))

    print(f"Created flights: {flight1.get_flight_number()}, {flight2.get_flight_number()}")

    # Add seats to flights
    seat_types = [SeatType.ECONOMY, SeatType.PREMIUM_ECONOMY, SeatType.BUSINESS, SeatType.FIRST_CLASS]
    seat_counts = [100, 30, 15, 5]  # Total: 150 seats

    for i, (seat_type, count) in enumerate(zip(seat_types, seat_counts)):
        for j in range(count):
            seat_number = f"{seat_type.value[0]}{j+1:02d}"
            seat = Seat(seat_number, seat_type)
            facade.add_seat_to_flight(flight1.get_flight_number(), seat)

    print(f"Added {len(facade.get_flight_seats(flight1.get_flight_number()))} seats to {flight1.get_flight_number()}")
    print(f"Available seats: {len(facade.get_available_seats(flight1.get_flight_number()))}")
    print(f"Flight status: {flight1.get_status().value}")
    print()

    # ==================== FLIGHT SEARCH DEMO ====================
    print("3. FLIGHT SEARCH")
    print("-" * 20)

    search_results = facade.search_flights("Delhi", "Mumbai", departure_time, seat_type=SeatType.BUSINESS, max_price=250.0)

    print(f"Found {len(search_results)} flights matching criteria")
    for result in search_results:
        flight = result["flight"]
        print(f"Flight: {flight.get_flight_number()}")
        print(f"Available seats: {result['total_available_seats']}")
        print(f"Price range: ₹{result['min_price']} - ₹{result['max_price']}\n")

    # ==================== BOOKING WORKFLOW DEMO ====================
    print("4. BOOKING WORKFLOW")
    print("-" * 25)

    # Search and lock seats
    try:
        print(f"Searching for flights between Delhi and Mumbai from {booking_start_date} to {booking_end_date}")
        locked_flight, locked_seats = facade.search_and_lock_seats(
            "Delhi", "Mumbai", 2, SeatType.BUSINESS, passenger1, booking_start_date, booking_end_date
        )
        print(f"Locked {len(locked_seats)} seats for {passenger1.get_name()}")
        print(f"Seats: {[seat.get_seat_number() for seat in locked_seats]}")

        # Calculate total price with decorators
        base_price = sum(seat.get_price() for seat in locked_seats)
        print(f"Base price: ₹{base_price}")

        # Apply price decorators
        price_component = BaseBookingPrice(base_price)
        price_component = TaxDecorator(price_component, 0.18)  # 18% GST
        price_component = ServiceChargeDecorator(price_component, 50.0)
        price_component = BaggageFeeDecorator(price_component, 100.0)
        price_component = AirPortFeeDecorator(price_component, 200.0)

        # Apply discount for frequent flyer
        if passenger1.get_passenger_type() == PassengerType.FREQUENT_FLYER:
            price_component = DiscountDecorator(price_component, 0.10)  # 10% discount

        final_price = price_component.get_price()
        print(f"Final price after taxes and fees: ₹{final_price:.2f}")

        # Process payment
        payment_strategy = CreditCardPaymentStrategy("1234-5678-9012-3456", "123", "12/25")
        payment_result = facade.process_payment(payment_strategy, final_price)

        if payment_result.get_payment_status().value == "SUCCESS":
            # Create booking
            booking = facade.create_booking(locked_flight, passenger1, locked_seats, payment_strategy, final_price)
            print(f"Booking created: {booking.get_booking_id()}")
            print(f"Booking status: {booking.get_status().value}")
        else:
            print("Payment failed!")

    except Exception as e:
        print(f"Booking failed: {e}")

    print()

    # ==================== MULTIPLE BOOKINGS DEMO ====================
    print("5. MULTIPLE BOOKINGS")
    print("-" * 25)

    # Book for passenger2
    try:
        locked_flight2, locked_seats2 = facade.search_and_lock_seats(
            "Delhi", "Mumbai", 1, SeatType.ECONOMY, passenger2, booking_start_date, booking_end_date
        )

        base_price2 = sum(seat.get_price() for seat in locked_seats2)
        price_component2 = BaseBookingPrice(base_price2)
        price_component2 = TaxDecorator(price_component2, 0.18)
        price_component2 = ServiceChargeDecorator(price_component2, 25.0)
        price_component2 = AirPortFeeDecorator(price_component2, 100.0)

        final_price2 = price_component2.get_price()

        payment_strategy2 = DebitCardPaymentStrategy("9876-5432-1098-7654")
        payment_result2 = facade.process_payment(payment_strategy2, final_price2)

        if payment_result2.get_payment_status().value == "SUCCESS":
            booking2 = facade.create_booking(locked_flight2, passenger2, locked_seats2, payment_strategy2, final_price2)
            print(f"Booking 2 created: {booking2.get_booking_id()}")
    except Exception as e:
        print(f"Booking 2 failed: {e}")

    # Book for passenger3
    try:
        locked_flight3, locked_seats3 = facade.search_and_lock_seats(
            "Delhi", "Mumbai", 1, SeatType.FIRST_CLASS, passenger3, booking_start_date, booking_end_date
        )

        base_price3 = sum(seat.get_price() for seat in locked_seats3)
        price_component3 = BaseBookingPrice(base_price3)
        price_component3 = TaxDecorator(price_component3, 0.18)
        price_component3 = ServiceChargeDecorator(price_component3, 100.0)
        price_component3 = BaggageFeeDecorator(price_component3, 200.0)
        price_component3 = AirPortFeeDecorator(price_component3, 500.0)

        # Corporate discount
        price_component3 = DiscountDecorator(price_component3, 0.15)

        final_price3 = price_component3.get_price()

        payment_strategy3 = BankTransferPaymentStrategy("CORP123456", "HDFC Bank")
        payment_result3 = facade.process_payment(payment_strategy3, final_price3)

        if payment_result3.get_payment_status().value == "SUCCESS":
            booking3 = facade.create_booking(locked_flight3, passenger3, locked_seats3, payment_strategy3, final_price3)
            print(f"Booking 3 created: {booking3.get_booking_id()}")
    except Exception as e:
        print(f"Booking 3 failed: {e}")

    print()

    # ==================== FLIGHT STATUS UPDATES ====================
    print("6. FLIGHT STATUS UPDATES")
    print("-" * 30)

    # Update flight status
    facade.update_flight_status(flight1.get_flight_number(), FlightStatus.SCHEDULED)
    print(f"Flight {flight1.get_flight_number()} status: {flight1.get_status().value}")

    facade.update_flight_status(flight1.get_flight_number(), FlightStatus.BOARDING)
    print(f"Flight {flight1.get_flight_number()} status: {flight1.get_status().value}")

    # Board passengers
    bookings = facade.get_bookings_by_flight(flight1)
    for booking in bookings:
        facade.board_passenger(booking.get_booking_id())
        print(f"Boarded passenger: {booking.get_passenger().get_name()}")

    facade.update_flight_status(flight1.get_flight_number(), FlightStatus.DEPARTED)
    print(f"Flight {flight1.get_flight_number()} status: {flight1.get_status().value}")

    facade.update_flight_status(flight1.get_flight_number(), FlightStatus.IN_AIR)
    print(f"Flight {flight1.get_flight_number()} status: {flight1.get_status().value}")

    facade.update_flight_status(flight1.get_flight_number(), FlightStatus.LANDED)
    print(f"Flight {flight1.get_flight_number()} status: {flight1.get_status().value}")

    print()

    # ==================== CANCELLATION DEMO ====================
    print("7. BOOKING CANCELLATION")
    print("-" * 30)

    # Create another booking to cancel
    try:
        locked_flight_cancel, locked_seats_cancel = facade.search_and_lock_seats(
            "Mumbai",
            "Bangalore",
            1,
            SeatType.ECONOMY,
            passenger1,
            departure_time + timedelta(hours=4) - timedelta(hours=1),
            arrival_time + timedelta(hours=4) + timedelta(hours=1),
        )

        base_price_cancel = sum(seat.get_price() for seat in locked_seats_cancel)
        price_component_cancel = BaseBookingPrice(base_price_cancel)
        price_component_cancel = TaxDecorator(price_component_cancel, 0.18)
        price_component_cancel = ServiceChargeDecorator(price_component_cancel, 25.0)
        price_component_cancel = AirPortFeeDecorator(price_component_cancel, 100.0)

        final_price_cancel = price_component_cancel.get_price()

        payment_strategy_cancel = CashPaymentStrategy()
        payment_result_cancel = facade.process_payment(payment_strategy_cancel, final_price_cancel)

        if payment_result_cancel.get_payment_status().value == "SUCCESS":
            booking_cancel = facade.create_booking(locked_flight_cancel, passenger1, locked_seats_cancel, payment_strategy_cancel, final_price_cancel)
            print(f"Created booking to cancel: {booking_cancel.get_booking_id()}")

            # Cancel the booking
            facade.cancel_booking(booking_cancel.get_booking_id())
            print(f"Cancelled booking: {booking_cancel.get_booking_id()}")
            print(f"Booking status: {booking_cancel.get_status().value}")

    except Exception as e:
        print(f"Cancellation demo failed: {e}")

    print()

    # ==================== FLIGHT COMPLETION ====================
    print("8. FLIGHT COMPLETION")
    print("-" * 25)

    facade.update_flight_status(flight1.get_flight_number(), FlightStatus.ARRIVED)
    print(f"Flight {flight1.get_flight_number()} status: {flight1.get_status().value}")

    facade.complete_flight(flight1.get_flight_number())
    print(f"Completed flight: {flight1.get_flight_number()}")

    print()

    # ==================== STATISTICS DEMO ====================
    print("9. SYSTEM STATISTICS")
    print("-" * 25)

    flight_stats = facade.get_flight_statistics()
    print("Flight Statistics:")
    print(f"Total flights: {flight_stats['total_flights']}")
    print(f"Total bookings: {flight_stats['total_bookings']}")
    print(f"Total revenue: ₹{flight_stats['total_revenue']:.2f}")
    print("Flights by status:")
    for status, count in flight_stats["flights_by_status"].items():
        print(f"  {status}: {count}")
    print("Bookings by status:")
    for status, count in flight_stats["bookings_by_status"].items():
        print(f"  {status}: {count}")

    print()

    user_stats = facade.get_user_statistics()
    print("User Statistics:")
    print(f"Total users: {user_stats['total_users']}")
    print("Users by type:")
    for user_type, count in user_stats["users_by_type"].items():
        print(f"  {user_type}: {count}")
    print("Passengers by type:")
    for passenger_type, count in user_stats["passengers_by_type"].items():
        print(f"  {passenger_type}: {count}")
    print("Staff by type:")
    for staff_type, count in user_stats["staff_by_type"].items():
        print(f"  {staff_type}: {count}")

    print()

    # ==================== SEAT STATUS DEMO ====================
    print("10. SEAT STATUS OVERVIEW")
    print("-" * 35)

    seats = facade.get_flight_seats(flight1.get_flight_number())
    seat_status_count = {}

    for seat in seats.values():
        status = seat.get_status().value
        seat_status_count[status] = seat_status_count.get(status, 0) + 1

    print(f"Seat status for flight {flight1.get_flight_number()}:")
    for status, count in seat_status_count.items():
        print(f"  {status}: {count}")

    print("\n=== DEMO COMPLETED ===")


if __name__ == "__main__":
    main()
