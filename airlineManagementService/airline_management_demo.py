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
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from airline_management import AirlineManagementFacade
from app.models.flight import Flight
from app.models.enums import PassengerType, StaffType, FlightStatus, SeatType, PaymentStatus
from app.models.seat import Seat
from app.models.payment_result import PaymentResult
from app.models.user import Passenger
from app.strategies.payment_strategy import CreditCardPaymentStrategy, DebitCardPaymentStrategy, CashPaymentStrategy, BankTransferPaymentStrategy
from app.decorators.booking_price_decorator import (
    BaseBookingPrice,
    TaxDecorator,
    ServiceChargeDecorator,
    BaggageFeeDecorator,
    DiscountDecorator,
    AirPortFeeDecorator,
)


def concurrent_booking_test(facade: AirlineManagementFacade, flight_number: str, seat_type: SeatType, num_users: int = 5):
    """Test concurrent booking for same seat type using ThreadPoolExecutor"""
    print(f"🚀 Testing {num_users} concurrent {seat_type.value} seat bookings...")

    # Create users for concurrent booking
    concurrent_users = []
    for i in range(num_users):
        user = facade.create_passenger(f"Concurrent User {i+1}", f"user{i+1}@concurrent.com", PassengerType.REGULAR)
        concurrent_users.append(user)

    # Results tracking
    results = {"successful_bookings": 0, "failed_bookings": 0, "booking_details": []}

    def attempt_booking(user: Passenger):
        """Function to be executed by each thread"""
        thread_id = threading.current_thread().ident
        try:
            # Search and lock seats - use the same date range as the main demo
            departure_time = datetime.now() + timedelta(days=1, hours=2)
            arrival_time = departure_time + timedelta(hours=3)
            booking_start_date = departure_time - timedelta(hours=1)
            booking_end_date = arrival_time + timedelta(hours=1)

            locked_flight, locked_seats = facade.search_and_lock_seats("Delhi", "Mumbai", 1, seat_type, user, booking_start_date, booking_end_date)

            if locked_seats:
                seat_number = locked_seats[0].get_seat_number()

                # Calculate price
                base_price = locked_seats[0].get_price()
                price_component = BaseBookingPrice(base_price)
                price_component = TaxDecorator(price_component, 0.18)
                price_component = ServiceChargeDecorator(price_component, 25.0)
                final_price = price_component.get_price()

                # Process payment
                payment_strategy = CreditCardPaymentStrategy(f"1234-{thread_id}", "123", "12/25")
                payment_result: PaymentResult = facade.process_payment(payment_strategy, final_price)

                if payment_result.get_payment_status() == PaymentStatus.SUCCESS:
                    # Create booking
                    booking = facade.create_booking(locked_flight, user, locked_seats, payment_strategy, final_price)
                    print(f"✅ {user.get_name()} → Seat {seat_number} → Booking {booking.get_booking_id()[:8]}...")

                    return {
                        "success": True,
                        "user": user.get_name(),
                        "seat": seat_number,
                        "booking_id": booking.get_booking_id(),
                        "thread_id": thread_id,
                    }
                else:
                    return {"success": False, "user": user.get_name(), "reason": "Payment failed", "thread_id": thread_id}
            else:
                return {"success": False, "user": user.get_name(), "reason": "No seats available", "thread_id": thread_id}

        except Exception as e:
            return {"success": False, "user": user.get_name(), "reason": str(e), "thread_id": thread_id}

    # Execute concurrent bookings using ThreadPoolExecutor
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=num_users) as executor:
        # Submit all booking tasks
        future_to_user = {executor.submit(attempt_booking, user): user for user in concurrent_users}

        # Collect results as they complete
        for future in as_completed(future_to_user):
            result = future.result()
            results["booking_details"].append(result)

            if result["success"]:
                results["successful_bookings"] += 1
            else:
                results["failed_bookings"] += 1

    end_time = time.time()
    execution_time = end_time - start_time

    # Print results summary
    print(f"📊 Results: {results['successful_bookings']}/{num_users} successful ({execution_time:.2f}s)")

    return results


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

    for seat_type, count in zip(seat_types, seat_counts):
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
        flight: Flight = result["flight"]
        print(f"Flight: {flight.get_flight_number()}")
        print(f"Available seats: {result['total_available_seats']}")
        print(f"Price range: ₹{result['min_price']} - ₹{result['max_price']}\n")

    # ==================== BOOKING WORKFLOW DEMO ====================
    print("4. BOOKING WORKFLOW")
    print("-" * 25)

    # Search and lock seats
    try:
        locked_flight, locked_seats = facade.search_and_lock_seats(
            "Delhi", "Mumbai", 2, SeatType.BUSINESS, passenger1, booking_start_date, booking_end_date
        )
        print(f"✅ {passenger1.get_name()} locked seats: {[seat.get_seat_number() for seat in locked_seats]}")

        # Calculate total price with decorators
        base_price = sum(seat.get_price() for seat in locked_seats)
        price_component = BaseBookingPrice(base_price)
        price_component = TaxDecorator(price_component, 0.18)  # 18% GST
        price_component = ServiceChargeDecorator(price_component, 50.0)
        price_component = BaggageFeeDecorator(price_component, 100.0)
        price_component = AirPortFeeDecorator(price_component, 200.0)

        # Apply discount for frequent flyer
        if passenger1.get_passenger_type() == PassengerType.FREQUENT_FLYER:
            price_component = DiscountDecorator(price_component, 0.10)  # 10% discount

        final_price = price_component.get_price()
        print(f"💰 Final price: ₹{final_price:.2f}")

        # Process payment
        payment_strategy = CreditCardPaymentStrategy("1234-5678-9012-3456", "123", "12/25")
        payment_result = facade.process_payment(payment_strategy, final_price)

        if payment_result.get_payment_status().value == "SUCCESS":
            booking = facade.create_booking(locked_flight, passenger1, locked_seats, payment_strategy, final_price)
            print(f"🎫 Booking created: {booking.get_booking_id()[:8]}... ({booking.get_status().value})")
        else:
            print("❌ Payment failed!")

    except Exception as e:
        print(f"❌ Booking failed: {e}")

    print()

    # ==================== TIMEOUT DEMONSTRATION ====================
    print("5. TIMEOUT DEMONSTRATION")
    print("-" * 30)

    # Create a new passenger for timeout demo
    timeout_passenger = facade.create_passenger("Timeout Demo User", "timeout@email.com", PassengerType.REGULAR)

    try:
        locked_flight_timeout, locked_seats_timeout = facade.search_and_lock_seats(
            "Delhi", "Mumbai", 1, SeatType.ECONOMY, timeout_passenger, booking_start_date, booking_end_date
        )
        print(f"🔒 Locked seat {locked_seats_timeout[0].get_seat_number()} - will auto-release in 2s...")

        # Wait for 3 seconds to see the timeout in action
        time.sleep(3)

        seat_status = locked_seats_timeout[0].get_status().value
        print(f"✅ Seat {locked_seats_timeout[0].get_seat_number()} status: {seat_status} (timeout cleanup successful)")

    except Exception as e:
        print(f"Timeout demo failed: {e}")

    print()

    # ==================== MULTIPLE BOOKINGS DEMO ====================
    print("6. MULTIPLE BOOKINGS")
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
            print(f"✅ {passenger2.get_name()} → Economy seat → ₹{final_price2:.2f}")
    except Exception as e:
        print(f"❌ {passenger2.get_name()} booking failed: {e}")

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
        price_component3 = DiscountDecorator(price_component3, 0.15)  # Corporate discount
        final_price3 = price_component3.get_price()

        payment_strategy3 = BankTransferPaymentStrategy("CORP123456", "HDFC Bank")
        payment_result3 = facade.process_payment(payment_strategy3, final_price3)

        if payment_result3.get_payment_status().value == "SUCCESS":
            booking3 = facade.create_booking(locked_flight3, passenger3, locked_seats3, payment_strategy3, final_price3)
            print(f"✅ {passenger3.get_name()} → First Class seat → ₹{final_price3:.2f}")
    except Exception as e:
        print(f"❌ {passenger3.get_name()} booking failed: {e}")

    print()

    # ==================== FLIGHT STATUS UPDATES ====================
    print("7. FLIGHT STATUS UPDATES")
    print("-" * 30)

    # Update flight status
    facade.update_flight_status(flight1.get_flight_number(), FlightStatus.SCHEDULED)
    facade.update_flight_status(flight1.get_flight_number(), FlightStatus.BOARDING)

    # Board passengers
    bookings = facade.get_bookings_by_flight(flight1)
    for booking in bookings:
        facade.board_passenger(booking.get_booking_id())

    facade.update_flight_status(flight1.get_flight_number(), FlightStatus.DEPARTED)
    facade.update_flight_status(flight1.get_flight_number(), FlightStatus.IN_AIR)
    facade.update_flight_status(flight1.get_flight_number(), FlightStatus.LANDED)

    print(f"✈️ Flight {flight1.get_flight_number()} completed journey: SCHEDULED → BOARDING → DEPARTED → IN_AIR → LANDED")

    print()

    # ==================== CANCELLATION DEMO ====================
    print("8. BOOKING CANCELLATION")
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
            facade.cancel_booking(booking_cancel.get_booking_id())
            print(f"✅ Booking cancelled: {booking_cancel.get_booking_id()[:8]}... ({booking_cancel.get_status().value})")

    except Exception as e:
        print(f"❌ Cancellation demo failed: {e}")

    print()

    # ==================== FLIGHT COMPLETION ====================
    print("9. FLIGHT COMPLETION")
    print("-" * 25)

    facade.update_flight_status(flight1.get_flight_number(), FlightStatus.ARRIVED)
    facade.complete_flight(flight1.get_flight_number())
    print(f"✅ Flight {flight1.get_flight_number()} completed successfully")

    print()

    # ==================== STATISTICS DEMO ====================
    print("10. SYSTEM STATISTICS")
    print("-" * 25)

    flight_stats = facade.get_flight_statistics()
    user_stats = facade.get_user_statistics()

    print(f"📊 System Overview:")
    print(f"  Flights: {flight_stats['total_flights']} | Bookings: {flight_stats['total_bookings']} | Revenue: ₹{flight_stats['total_revenue']:.2f}")
    print(
        f"  Users: {user_stats['total_users']} | Passengers: {user_stats['users_by_type']['PASSENGER']} | Staff: {user_stats['users_by_type']['AIRLINE_STAFF']}"
    )

    print()

    # ==================== CONCURRENCY TEST ====================
    print("11. CONCURRENCY TEST")
    print("-" * 25)

    # Test concurrent booking for Business class seats (limited availability)
    concurrent_results = concurrent_booking_test(facade, flight1.get_flight_number(), SeatType.BUSINESS, num_users=5)

    # Test concurrent booking for Economy class seats (more availability)
    concurrent_results_economy = concurrent_booking_test(facade, flight1.get_flight_number(), SeatType.ECONOMY, num_users=3)

    print()

    # ==================== SEAT STATUS DEMO ====================
    print("12. SEAT STATUS OVERVIEW")
    print("-" * 35)

    seats = facade.get_flight_seats(flight1.get_flight_number())
    seat_status_count = {}

    for seat in seats.values():
        status = seat.get_status().value
        seat_status_count[status] = seat_status_count.get(status, 0) + 1

    print(f"🪑 Seat Status: {', '.join([f'{status}: {count}' for status, count in seat_status_count.items()])}")

    print("\n=== DEMO COMPLETED ===")


if __name__ == "__main__":
    main()
