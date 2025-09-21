"""
Movie Ticket Booking Service Demo
================================

This script demonstrates the complete functionality of the Movie Ticket Booking Service
including user management, movie management, show creation, seat booking, payment processing,
and various design patterns like Observer, Strategy, and State patterns.
"""

from app.movie_ticket_booking_service import MovieTicketBookingService
from app.models.user import User
from app.models.movie import Movie
from app.models.show import Show
from app.models.seat import Seat
from app.models.cinema import Cinema
from app.models.screen import Screen
from app.models.enums import Genre, SeatType
from app.models.strategy.payment_strategy import CreditCardPaymentStrategy, CashPaymentStrategy, UPIPaymentStrategy
from app.models.strategy.show_pricing_strategy import MorningPricingStrategy, EveningPricingStrategy, WeekendPricingStrategy, VipPricingStrategy
from datetime import datetime, timedelta
import random
import time


class MovieTicketBookingServiceDemo:
    """Demo class to showcase the Movie Ticket Booking Service functionality."""

    def __init__(self):
        """Initialize the demo with the singleton service instance."""
        self.movie_ticket_booking_service = MovieTicketBookingService.get_instance()
        print("🎬 Movie Ticket Booking Service Demo Started!")
        print("=" * 50)

    def run(self):
        """Run the complete demo showcasing all features."""
        try:
            self._setup_users()
            self._setup_movies()
            self._setup_cinemas_and_screens()
            self._setup_shows()
            self._demonstrate_observer_pattern()
            self._demonstrate_booking_scenarios()
            self._demonstrate_payment_strategies()
            self._demonstrate_search_functionality()
            self._demonstrate_booking_management()
            self._demonstrate_error_scenarios()

            print("\n🎉 Demo completed successfully!")
            print("=" * 50)

        except Exception as e:
            print(f"❌ Demo failed with error: {e}")
            raise

    def _setup_users(self):
        """Create and register users in the system."""
        print("\n👥 Setting up users...")

        users = [
            User("Amit Kumar", "amit@example.com"),
            User("Rajesh Singh", "rajesh@example.com"),
            User("Suresh Patel", "suresh@example.com"),
            User("Priya Sharma", "priya@example.com"),
            User("Anita Gupta", "anita@example.com"),
        ]

        for user in users:
            self.movie_ticket_booking_service.add_user(user)
            print(f"✅ User registered: {user.get_name()} ({user.get_email()})")

        print(f"Total users registered: {len(users)}")

    def _setup_movies(self):
        """Create and add movies to the system."""
        print("\n🎬 Setting up movies...")

        movies = [
            Movie("War", Genre.ACTION, 110),
            Movie("Phir Hera Pheri", Genre.COMEDY, 115),
            Movie("Taare Zameen Par", Genre.DRAMA, 120),
            Movie("Dilwale Dulhania Le Jayenge", Genre.ROMANCE, 125),
            Movie("Andhadhun", Genre.THRILLER, 130),
            Movie("Interstellar", Genre.SCIENCE_FICTION, 169),
            Movie("The Conjuring", Genre.HORROR, 112),
            Movie("Frozen", Genre.ANIMATION, 102),
        ]

        for movie in movies:
            self.movie_ticket_booking_service.add_movie(movie)
            print(f"✅ Movie added: {movie.title} ({movie.genre.value}) - {movie.get_duration()} min")

        print(f"Total movies added: {len(movies)}")

    def _setup_cinemas_and_screens(self):
        """Create cinemas and screens with seats."""
        print("\n🏢 Setting up cinemas and screens...")

        # Create seats for screens
        all_available_seats = []
        for i in range(30):  # 3 rows x 10 columns
            row = i // 10
            col = i % 10
            if i < 10:
                seat_type = SeatType.REGULAR
            elif i < 20:
                seat_type = SeatType.PREMIUM
            else:
                seat_type = SeatType.RECLINER

            all_available_seats.append(Seat(row, col, seat_type))

        # Create screens
        screens = []
        for i in range(3):
            screen = Screen(f"Screen {i+1}", all_available_seats.copy())
            screens.append(screen)
            print(f"✅ Screen created: {screen.name} with {len(screen.seats)} seats")

        # Create cinemas
        cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad"]

        for i in range(2):
            city = random.choice(cities)
            cinema = Cinema(f"Cinema {i+1}", city, screens)
            self.movie_ticket_booking_service.add_cinema(cinema)
            print(f"✅ Cinema created: {cinema.name} in {cinema.city}")

        print(f"Total cinemas: 2, Total screens: {len(screens)}")

    def _setup_shows(self):
        """Create shows with different pricing strategies."""
        print("\n🎭 Setting up shows...")

        # Get movies and cinemas
        movies = list(self.movie_ticket_booking_service.movie.values())
        cinemas = list(self.movie_ticket_booking_service.cinema.values())

        # Create shows with different pricing strategies
        shows = []
        base_time = datetime.now() + timedelta(hours=1)

        for i, movie in enumerate(movies[:6]):  # Use first 6 movies
            cinema = cinemas[i % len(cinemas)]
            screen = cinema.screens[i % len(cinema.screens)]

            # Different pricing strategies based on time
            if i % 4 == 0:
                pricing_strategy = MorningPricingStrategy()
                show_time = base_time + timedelta(hours=i * 2)
            elif i % 4 == 1:
                pricing_strategy = EveningPricingStrategy()
                show_time = base_time + timedelta(hours=i * 2)
            elif i % 4 == 2:
                pricing_strategy = WeekendPricingStrategy()
                show_time = base_time + timedelta(hours=i * 2)
            else:
                pricing_strategy = VipPricingStrategy()
                show_time = base_time + timedelta(hours=i * 2)

            show = Show(f"Show {i+1}", movie, screen, show_time, pricing_strategy)
            shows.append(show)
            self.movie_ticket_booking_service.add_show(show)

            print(f"✅ Show created: {show.name} - {movie.title} at {show_time.strftime('%H:%M')} ({pricing_strategy.__class__.__name__})")

        print(f"Total shows created: {len(shows)}")

    def _demonstrate_observer_pattern(self):
        """Demonstrate the Observer pattern with movie releases."""
        print("\n👀 Demonstrating Observer Pattern (Movie Release Notifications)...")

        # Get users and movies
        users = list(self.movie_ticket_booking_service.user_service.users.values())
        movies = list(self.movie_ticket_booking_service.movie.values())

        # Subscribe users to movies
        movies[0].add_observer(users[0])  # Amit subscribes to War
        movies[0].add_observer(users[1])  # Rajesh subscribes to War
        movies[1].add_observer(users[2])  # Suresh subscribes to Phir Hera Pheri
        movies[2].add_observer(users[0])  # Amit subscribes to Taare Zameen Par
        movies[2].add_observer(users[1])  # Rajesh subscribes to Taare Zameen Par
        movies[2].add_observer(users[2])  # Suresh subscribes to Taare Zameen Par

        print("📧 Users subscribed to movie notifications:")
        print(f"   - {users[0].get_name()} subscribed to: War, Taare Zameen Par")
        print(f"   - {users[1].get_name()} subscribed to: War, Taare Zameen Par")
        print(f"   - {users[2].get_name()} subscribed to: Phir Hera Pheri, Taare Zameen Par")

        # Release movies to trigger notifications
        print("\n🎬 Releasing movies...")
        movies[0].release_movie()  # War
        time.sleep(0.5)  # Small delay for better output
        movies[1].release_movie()  # Phir Hera Pheri
        time.sleep(0.5)
        movies[2].release_movie()  # Taare Zameen Par

    def _demonstrate_booking_scenarios(self):
        """Demonstrate various booking scenarios."""
        print("\n🎫 Demonstrating Booking Scenarios...")

        # Get users and shows
        users = list(self.movie_ticket_booking_service.user_service.users.values())
        shows = list(self.movie_ticket_booking_service.show.values())

        # Scenario 1: Successful booking
        print("\n📝 Scenario 1: Successful booking")
        user = users[0]
        show = shows[0]
        seats = show.screen.seats[:3]  # First 3 seats

        print(f"   User: {user.get_name()}")
        print(f"   Show: {show.name} - {show.movie.title}")
        print(f"   Seats: {[f'Row {seat.row}, Col {seat.col}' for seat in seats]}")

        payment_strategy = CreditCardPaymentStrategy("1234-5678-9012-3456", "123", "12/25")
        booking = self.movie_ticket_booking_service.book_tickets(user, show, seats, payment_strategy)

        if booking:
            print(f"   ✅ Booking successful! Booking ID: {booking.id}")
            print(f"   Total price: ₹{booking.total_price}")
        else:
            print("   ❌ Booking failed!")

    def _demonstrate_payment_strategies(self):
        """Demonstrate different payment strategies."""
        print("\n💳 Demonstrating Payment Strategies...")

        users = list(self.movie_ticket_booking_service.user_service.users.values())
        shows = list(self.movie_ticket_booking_service.show.values())

        # Credit Card Payment
        print("\n💳 Credit Card Payment:")
        user = users[1]
        show = shows[1]
        seats = show.screen.seats[3:5]  # Seats 4-5

        payment_strategy = CreditCardPaymentStrategy("9876-5432-1098-7654", "456", "06/26")
        booking = self.movie_ticket_booking_service.book_tickets(user, show, seats, payment_strategy)

        if booking:
            print(f"   ✅ Credit card payment successful! Booking ID: {booking.id}")

        # UPI Payment
        print("\n📱 UPI Payment:")
        user = users[2]
        show = shows[2]
        seats = show.screen.seats[5:7]  # Seats 6-7

        payment_strategy = UPIPaymentStrategy("rajesh@paytm")
        booking = self.movie_ticket_booking_service.book_tickets(user, show, seats, payment_strategy)

        if booking:
            print(f"   ✅ UPI payment successful! Booking ID: {booking.id}")

        # Cash Payment
        print("\n💰 Cash Payment:")
        user = users[3]
        show = shows[3]
        seats = show.screen.seats[7:9]  # Seats 8-9

        payment_strategy = CashPaymentStrategy()
        booking = self.movie_ticket_booking_service.book_tickets(user, show, seats, payment_strategy)

        if booking:
            print(f"   ✅ Cash payment successful! Booking ID: {booking.id}")

    def _demonstrate_search_functionality(self):
        """Demonstrate search functionality."""
        print("\n🔍 Demonstrating Search Functionality...")

        # Search by movie name
        print("\n🎬 Searching for movies containing 'War':")
        movies = self.movie_ticket_booking_service.search_service.search_movies_by_name("War")
        for movie in movies:
            print(f"   - {movie.title} ({movie.genre.value})")

        # Search by genre
        print("\n🎭 Searching for ACTION movies:")
        movies = self.movie_ticket_booking_service.search_service.search_movies_by_genre(Genre.ACTION)
        for movie in movies:
            print(f"   - {movie.title} ({movie.genre.value})")

        # Search shows by city
        print("\n🏙️ Searching for shows in Mumbai:")
        shows = self.movie_ticket_booking_service.search_service.search_shows_by_city("Mumbai")
        for show in shows:
            print(f"   - {show.name}: {show.movie.title} at {show.show_time.strftime('%H:%M')}")

    def _demonstrate_booking_management(self):
        """Demonstrate booking management features."""
        print("\n📋 Demonstrating Booking Management...")

        users = list(self.movie_ticket_booking_service.user_service.users.values())

        # Show booking history
        for user in users[:3]:  # Show history for first 3 users
            bookings = user.get_booking_history()
            print(f"\n📚 Booking history for {user.get_name()}:")
            if bookings:
                for booking in bookings:
                    print(f"   - Booking {booking.id}: {booking.show.movie.title} ({booking.status.value})")
            else:
                print("   No bookings found")

    def _demonstrate_error_scenarios(self):
        """Demonstrate error handling scenarios."""
        print("\n⚠️ Demonstrating Error Scenarios...")

        # Try to book already booked seats
        print("\n🚫 Attempting to book already booked seats:")
        users = list(self.movie_ticket_booking_service.user_service.users.values())
        shows = list(self.movie_ticket_booking_service.show.values())

        user = users[4]
        show = shows[0]
        seats = show.screen.seats[:3]  # These should be already booked

        payment_strategy = CreditCardPaymentStrategy("1111-2222-3333-4444", "999", "12/25")
        booking = self.movie_ticket_booking_service.book_tickets(user, show, seats, payment_strategy)

        if not booking:
            print("   ✅ System correctly prevented double booking!")

        # Try to get non-existent user
        print("\n👤 Attempting to get non-existent user:")
        try:
            self.movie_ticket_booking_service.get_user("non-existent-id")
        except ValueError as e:
            print(f"   ✅ System correctly handled error: {e}")

        # Try to get non-existent show
        print("\n🎭 Attempting to get non-existent show:")
        try:
            self.movie_ticket_booking_service.get_show("non-existent-id")
        except ValueError as e:
            print(f"   ✅ System correctly handled error: {e}")

    def _print_system_summary(self):
        """Print a summary of the system state."""
        print("\n📊 System Summary:")
        print(f"   Users: {len(self.movie_ticket_booking_service.user_service.users)}")
        print(f"   Movies: {len(self.movie_ticket_booking_service.movie)}")
        print(f"   Cinemas: {len(self.movie_ticket_booking_service.cinema)}")
        print(f"   Shows: {len(self.movie_ticket_booking_service.show)}")

        total_bookings = sum(len(user.get_booking_history()) for user in self.movie_ticket_booking_service.user_service.users.values())
        print(f"   Total Bookings: {total_bookings}")


def main():
    """Main function to run the demo."""
    print("🎬 Welcome to the Movie Ticket Booking Service Demo!")
    print("This demo showcases various design patterns and system features.")
    print("=" * 60)

    demo = MovieTicketBookingServiceDemo()
    demo.run()
    demo._print_system_summary()

    print("\n🎉 Thank you for using the Movie Ticket Booking Service Demo!")
    print("=" * 60)


if __name__ == "__main__":
    main()
