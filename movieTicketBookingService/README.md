# 🎬 Movie Ticket Booking Service

A comprehensive Python-based movie ticket booking system that demonstrates various design patterns and software engineering principles. This project showcases a real-world application with clean architecture, proper separation of concerns, and extensive use of design patterns.

## 📋 Table of Contents

- [Features](#features)
- [Design Patterns](#design-patterns)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Design Pattern Explanations](#design-pattern-explanations)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality

- **User Management**: User registration, profile management, and booking history
- **Movie Management**: Movie catalog with genres, duration, and release notifications
- **Cinema & Screen Management**: Multi-cinema support with multiple screens per cinema
- **Show Management**: Time-based show scheduling with different pricing strategies
- **Seat Management**: Different seat types (Regular, Premium, Recliner) with availability tracking
- **Booking System**: Complete booking workflow with seat locking and confirmation
- **Payment Processing**: Multiple payment methods (Credit Card, UPI, Cash)
- **Search & Discovery**: Search movies by name, genre, and shows by city
- **Real-time Notifications**: Observer pattern for movie releases and booking updates

### Advanced Features

- **Seat Locking**: Prevents double booking with timeout-based seat locking
- **Concurrent Booking**: Thread-safe booking operations
- **State Management**: Booking state transitions (Pending → Confirmed → Cancelled)
- **Dynamic Pricing**: Different pricing strategies based on show timing
- **Error Handling**: Comprehensive error handling and validation
- **Observer Notifications**: Real-time updates for movie releases and booking status

## 🏗️ Design Patterns

This project demonstrates the following design patterns:

### 1. **Singleton Pattern**

- **Implementation**: `MovieTicketBookingService`
- **Purpose**: Ensures only one instance of the booking service exists
- **Benefits**: Centralized state management, resource optimization

### 2. **Observer Pattern**

- **Implementation**: Movie release notifications, booking status updates
- **Components**: `MovieSubject`, `MovieObserver`, `User` (observer)
- **Benefits**: Loose coupling, real-time notifications

### 3. **Strategy Pattern**

- **Implementation**: Payment methods, pricing strategies
- **Components**: `PaymentStrategy`, `ShowPricingStrategy`
- **Benefits**: Easy addition of new payment methods and pricing models

### 4. **State Pattern**

- **Implementation**: Booking state management
- **Components**: `BookingState`, `PendingState`, `ConfirmedState`, `CancelledState`
- **Benefits**: Clean state transitions, behavior encapsulation

### 5. **Factory Pattern**

- **Implementation**: User and movie creation
- **Benefits**: Centralized object creation, consistent initialization

### 6. **Facade Pattern**

- **Implementation**: `MovieTicketBookingService` as a simplified interface
- **Benefits**: Simplified client interface, subsystem complexity hiding

## 📁 Project Structure

```
movieTicketBookingService/
├── app/
│   ├── models/
│   │   ├── observer/
│   │   │   └── movie_observer.py      # Observer pattern implementation
│   │   ├── strategy/
│   │   │   ├── payment_strategy.py    # Payment strategy pattern
│   │   │   └── show_pricing_strategy.py # Pricing strategy pattern
│   │   ├── booking.py                 # Booking model with state pattern
│   │   ├── booking_state.py           # State pattern implementation
│   │   ├── cinema.py                  # Cinema model
│   │   ├── enums.py                   # Enumerations and constants
│   │   ├── movie.py                   # Movie model with observer
│   │   ├── payment.py                 # Payment result model
│   │   ├── screen.py                  # Screen model
│   │   ├── seat.py                    # Seat model
│   │   ├── show.py                    # Show model
│   │   └── user.py                    # User model with observer
│   ├── services/
│   │   ├── booking_service.py         # Booking business logic
│   │   ├── payment_service.py         # Payment processing
│   │   ├── search_service.py          # Search functionality
│   │   └── user_service.py            # User management
│   ├── movie_ticket_booking_service.py # Main service (Singleton + Facade)
│   └── seat_lock_manager.py           # Seat locking mechanism
├── run.py                             # Demo script
└── README.md                          # This file
```

## 🔧 Prerequisites

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 4GB RAM (for concurrent operations)
- **Dependencies**: Only Python standard library (no external dependencies)

## 🚀 Installation & Setup

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd movieTicketBookingService

# Or download and extract the project folder
```

### 2. Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Verify Installation

```bash
python --version  # Should be 3.8+
```

## 🎯 Usage

### Quick Start

```bash
# Run the demo
python run.py
```

### Basic Usage Examples

#### 1. Create and Run the Service

```python
from app.movie_ticket_booking_service import MovieTicketBookingService
from app.models.user import User
from app.models.movie import Movie
from app.models.enums import Genre

# Get service instance (Singleton)
service = MovieTicketBookingService.get_instance()

# Create and add users
user = User("John Doe", "john@example.com")
service.add_user(user)

# Create and add movies
movie = Movie("Inception", Genre.SCIENCE_FICTION, 148)
service.add_movie(movie)
```

#### 2. Book Tickets

```python
from app.models.strategy.payment_strategy import CreditCardPaymentStrategy

# Get user and show
user = service.get_user(user_id)
show = service.get_show(show_id)

# Select seats
seats = show.screen.seats[:3]  # First 3 seats

# Create payment strategy
payment = CreditCardPaymentStrategy("1234-5678-9012-3456", "123", "12/25")

# Book tickets
booking = service.book_tickets(user, show, seats, payment)
```

#### 3. Search Movies

```python
# Search by name
movies = service.search_service.search_movies_by_name("Inception")

# Search by genre
action_movies = service.search_service.search_movies_by_genre(Genre.ACTION)

# Search shows by city
mumbai_shows = service.search_service.search_shows_by_city("Mumbai")
```

## 📚 API Reference

### Core Service Methods

#### User Management

```python
# Add user
service.add_user(user: User) -> None

# Get user
service.get_user(user_id: str) -> User

# Get all users
service.user_service.get_all_users() -> list[User]
```

#### Movie Management

```python
# Add movie
service.add_movie(movie: Movie) -> None

# Get movie
service.get_movie(movie_id: str) -> Movie
```

#### Show Management

```python
# Add show
service.add_show(show: Show) -> None

# Get show
service.get_show(show_id: str) -> Show
```

#### Booking Operations

```python
# Book tickets
service.book_tickets(user: User, show: Show, seats: list[Seat], payment_strategy: PaymentStrategy) -> Optional[Booking]

# Cancel booking
service.cancel_booking(booking: Booking) -> None
```

### Data Models

#### User

```python
class User:
    def __init__(self, name: str, email: str)
    def get_name(self) -> str
    def get_email(self) -> str
    def get_booking_history(self) -> list[Booking]
```

#### Movie

```python
class Movie:
    def __init__(self, title: str, genre: Genre, duration_in_minutes: int)
    def release_movie(self) -> None  # Triggers observer notifications
```

#### Booking

```python
class Booking:
    def __init__(self, user: User, show: Show, seats: list[Seat])
    def confirm_booking(self) -> bool
    def cancel_booking(self) -> bool
```

## 📊 Entity Relationship Diagram

### Core Entities and Relationships

```
┌─────────────────────────────────────┐
│ MovieTicketBookingService           │
│─────────────────────────────────────│
│ (Singleton/Facade)                  │
│ - payment_service                   │
│ - search_service                    │
│ - booking_service                   │
│ - user_service                      │
│ - cinema (Dict)                     │
│ - show (Dict)                       │
│ - movie (Dict)                      │
└──────┬──────────────────────────────┘
       │
       │ 1..* (manages)
       │
       ▼
┌─────────────────────────────────────┐
│            User                     │
│─────────────────────────────────────│
│ id                                  │
│ name                                │
│ email                               │
│ booking_history (List<Booking>)     │
└──────┬──────────────────────────────┘
       │
       │ 1..* (has)
       │
       ▼
┌─────────────────────────────────────┐
│          Booking                    │
│─────────────────────────────────────│
│ id                                  │
│ user (User)                         │
│ show (Show)                         │
│ seats (List<Seat>)                  │
│ state (BookingState)                │
│ status (BookingStatus)              │
│ total_price                         │
└──────┬──────────────────────────────┘
       │
       │ references
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│    Show     │ │    Seat     │ │   Movie     │
└─────────────┘ └─────────────┘ └─────────────┘

┌─────────────────────────────────────┐
│            Movie                    │
│─────────────────────────────────────│
│ id                                  │
│ title                               │
│ genre (Genre)                       │
│ duration_in_minutes                 │
│ observers (List<Observer>)          │
└──────┬──────────────────────────────┘
       │
       │ 1..* (shown in)
       │
       ▼
┌─────────────────────────────────────┐
│            Show                     │
│─────────────────────────────────────│
│ id                                  │
│ movie (Movie)                       │
│ screen (Screen)                     │
│ show_time                           │
│ pricing_strategy                    │
└──────┬──────────────────────────────┘
       │
       │ 1 (has)
       │
       ▼
┌─────────────────────────────────────┐
│           Screen                    │
│─────────────────────────────────────│
│ id                                  │
│ cinema (Cinema)                     │
│ seats (List<Seat>)                  │
└──────┬──────────────────────────────┘
       │
       │ 1 (belongs to)
       │
       ▼
┌─────────────────────────────────────┐
│           Cinema                    │
│─────────────────────────────────────│
│ id                                  │
│ name                                │
│ city                                │
│ screens (List<Screen>)              │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│            Seat                     │
│─────────────────────────────────────│
│ id                                  │
│ seat_number                         │
│ type (SeatType)                     │
│ status (SeatStatus)                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│        BookingState                 │
│─────────────────────────────────────│
│ (Abstract)                          │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼
┌─────────────┐ ┌──────────────┐ ┌──────────────┐
│ PendingState│ │ConfirmedState│ │CancelledState│
└─────────────┘ └──────────────┘ └──────────────┘
```

### Entity Relationships

1. **MovieTicketBookingService ↔ User** (One-to-Many)

   - Service manages multiple Users
   - Users stored in UserService

2. **User ↔ Booking** (One-to-Many)

   - A User can have multiple Bookings
   - Each Booking belongs to one User
   - User maintains booking_history

3. **Booking ↔ Show** (Many-to-One)

   - A Booking is for one Show
   - A Show can have multiple Bookings

4. **Booking ↔ Seat** (One-to-Many)

   - A Booking can include multiple Seats
   - Each Seat can be in one active Booking

5. **Show ↔ Movie** (Many-to-One)

   - A Show displays one Movie
   - A Movie can be shown in multiple Shows

6. **Show ↔ Screen** (Many-to-One)

   - A Show is shown on one Screen
   - A Screen can host multiple Shows (at different times)

7. **Screen ↔ Cinema** (Many-to-One)

   - A Screen belongs to one Cinema
   - A Cinema has multiple Screens

8. **Screen ↔ Seat** (One-to-Many)

   - A Screen has multiple Seats
   - Each Seat belongs to one Screen

9. **Booking ↔ BookingState** (One-to-One)

   - Each Booking has one current State
   - State transitions: Pending → Confirmed → Cancelled

10. **Observer Pattern Relationships**

    - Movie implements `MovieSubject` - notifies on release
    - User implements `MovieObserver` - receives movie release notifications

11. **Strategy Pattern Relationships**
    - Show uses `ShowPricingStrategy` (delegates price calculation)
    - PaymentService uses `PaymentStrategy` (delegates payment processing)

## 🔄 Data Flow Diagrams

### 1. Movie Release Flow

```
┌──────────┐
│  Admin   │
└────┬─────┘
     │
     │ 1. release_movie()
     ▼
┌─────────────────┐
│     Movie       │
└────┬────────────┘
     │
     │ 2. notify_observers()
     ▼
┌─────────────────┐
│  All Observers  │
│  (Users)        │
└────┬────────────┘
     │
     │ 3. update_movie_status()
     ▼
┌─────────────────┐
│     Users       │
│  (Notified)     │
└─────────────────┘
```

### 2. Booking Creation Flow

```
┌──────────┐
│   User   │
└────┬─────┘
     │
     │ 1. book_tickets(user, show, seats, payment)
     ▼
┌─────────────────┐
│BookingService   │
└────┬────────────┘
     │
     │ 2. Lock seats
     │ 3. Validate availability
     ▼
┌─────────────────┐
│ SeatLockManager │
└────┬────────────┘
     │
     │ 4. Process payment
     ▼
┌─────────────────┐
│ PaymentService  │
└────┬────────────┘
     │
     │ 5. Create Booking
     │ 6. Update seat status
     ▼
┌─────────────────┐
│    Booking      │
│  - Seats        │
│  - State        │
└────┬────────────┘
     │
     │ 7. Add to user history
     ▼
┌─────────────────┐
│     User        │
│  (Updated)      │
└─────────────────┘
```

### 3. Search Flow

```
┌──────────┐
│   User   │
└────┬─────┘
     │
     │ 1. search_movies_by_name/genre()
     │    search_shows_by_city()
     ▼
┌─────────────────┐
│ SearchService   │
└────┬────────────┘
     │
     │ 2. Query movies/shows
     │ 3. Filter results
     ▼
┌─────────────────┐
│  Results        │
│  (Movies/Shows) │
└─────────────────┘
```

### 4. Complete System Interaction Flow

```
┌──────────────┐
│   Client     │
│  (run.py)    │
└──────┬───────┘
       │
       │ All Operations
       ▼
┌─────────────────────────────────────┐
│ MovieTicketBookingService           │
│ (Singleton/Facade)                  │
│  - User Management                  │
│  - Movie Management                 │
│  - Booking Management               │
│  - Search Management                │
└──────┬──────────────────────────────┘
       │
       ├──────────────────┬──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ UserService │  │BookingService│ │SearchService│
│             │  │             │  │             │
└─────────────┘  └─────────────┘  └─────────────┘
       │                  │                  │
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Users     │  │  Bookings   │  │  Movies     │
│             │  │  - Shows    │  │  - Shows    │
│             │  │  - Seats    │  │  - Screens  │
└─────────────┘  └─────────────┘  └─────────────┘
       │                  │                  │
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐  ┌───────────────┐  ┌───────────────┐
│ BookingState│  │PaymentStrategy│  │PricingStrategy│
│  (State     │  │  (Strategy)   │  │  (Strategy)   │
│   Pattern)  │  │               │  │               │
└─────────────┘  └───────────────┘  └───────────────┘
```

## 📋 Entity Attributes Summary

### User Entity

- `id`: Unique identifier (UUID)
- `name`: User's full name
- `email`: User's email address
- `booking_history`: List of Booking objects

### Movie Entity

- `id`: Unique identifier (UUID)
- `title`: Movie title
- `genre`: Genre enum
- `duration_in_minutes`: Movie duration
- `observers`: List of Observer objects

### Cinema Entity

- `id`: Unique identifier (UUID)
- `name`: Cinema name
- `city`: City location
- `screens`: List of Screen objects

### Screen Entity

- `id`: Unique identifier (UUID)
- `cinema`: Reference to Cinema
- `seats`: List of Seat objects

### Show Entity

- `id`: Unique identifier (UUID)
- `movie`: Reference to Movie
- `screen`: Reference to Screen
- `show_time`: Show timing
- `pricing_strategy`: ShowPricingStrategy object

### Seat Entity

- `id`: Unique identifier (UUID)
- `seat_number`: Seat identifier
- `type`: SeatType (REGULAR, PREMIUM, RECLINER)
- `status`: SeatStatus (AVAILABLE, BOOKED)

### Booking Entity

- `id`: Unique identifier (UUID)
- `user`: Reference to User
- `show`: Reference to Show
- `seats`: List of Seat objects
- `state`: BookingState object
- `status`: BookingStatus (PENDING, CONFIRMED, CANCELLED)
- `total_price`: Total booking price

## 🎨 Design Pattern Explanations

### 1. Singleton Pattern

```python
class MovieTicketBookingService:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

**Why**: Ensures single point of control for the booking system, prevents multiple instances that could lead to data inconsistency.

### 2. Observer Pattern

```python
# Movie releases notify all subscribed users
movie.add_observer(user1)
movie.add_observer(user2)
movie.release_movie()  # All observers get notified
```

**Why**: Loose coupling between movie releases and user notifications. Easy to add/remove subscribers without modifying the movie class.

### 3. Strategy Pattern

```python
# Different payment methods
credit_card = CreditCardPaymentStrategy("1234-5678", "123", "12/25")
upi = UPIPaymentStrategy("user@paytm")
cash = CashPaymentStrategy()

# Same interface, different implementations
payment_result = strategy.pay(amount)
```

**Why**: Easy to add new payment methods without modifying existing code. Each payment method encapsulates its own logic.

### 4. State Pattern

```python
# Booking states
pending_state = PendingState()
confirmed_state = ConfirmedState()
cancelled_state = CancelledState()

# State transitions
booking.state = pending_state
booking.confirm_booking()  # Transitions to confirmed_state
```

**Why**: Clean separation of behavior based on state. Easy to add new states and transitions.

## 🧪 Testing

### Run the Demo

```bash
python run.py
```

### Test Individual Components

```python
# Test user creation
from app.models.user import User
user = User("Test User", "test@example.com")
assert user.get_name() == "Test User"

# Test movie creation
from app.models.movie import Movie
from app.models.enums import Genre
movie = Movie("Test Movie", Genre.ACTION, 120)
assert movie.title == "Test Movie"
```

### Expected Demo Output

The demo should show:

- User registration and movie setup
- Observer pattern notifications
- Successful booking scenarios
- Different payment methods
- Search functionality
- Error handling scenarios
- System summary

## 🔧 Configuration

### Seat Types and Pricing

```python
# Modify in app/models/enums.py
class SeatType(Enum):
    REGULAR = (50.0, "REGULAR")      # ₹50
    PREMIUM = (80.0, "PREMIUM")      # ₹80
    RECLINER = (120.0, "RECLINER")   # ₹120
```

### Seat Lock Timeout

```python
# Modify in app/seat_lock_manager.py
self.lock_timeout = 2  # seconds
```

### Pricing Strategies

```python
# Modify in app/models/strategy/show_pricing_strategy.py
class MorningPricingStrategy(ShowPricingStrategy):
    def calculate_price(self, base_price: float) -> float:
        return base_price * 0.8  # 20% discount
```

## 🚀 Extending the System

### Adding New Payment Methods

```python
class PayPalPaymentStrategy(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> PaymentResult:
        # PayPal payment logic
        return PaymentResult(amount, PaymentStatus.SUCCESS, "PayPal payment successful")
```

### Adding New Pricing Strategies

```python
class HolidayPricingStrategy(ShowPricingStrategy):
    def calculate_price(self, base_price: float) -> float:
        return base_price * 1.5  # 50% premium for holidays
```

### Adding New Search Criteria

```python
def search_shows_by_time(self, start_time: datetime, end_time: datetime) -> list[Show]:
    return [show for show in self.shows
            if start_time <= show.show_time <= end_time]
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors

```
ModuleNotFoundError: No module named 'app'
```

**Solution**: Ensure you're running from the correct directory and Python path is set correctly.

#### 2. Circular Import Issues

```
ImportError: cannot import name 'Movie' from partially initialized module
```

**Solution**: Use `TYPE_CHECKING` and forward references for type hints.

#### 3. Property Setter Errors

```
TypeError: 'SeatStatus' object is not callable
```

**Solution**: Use regular methods instead of property setters for complex operations.

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Considerations

### Memory Usage

- **Users**: ~1KB per user
- **Movies**: ~500B per movie
- **Bookings**: ~2KB per booking
- **Seats**: ~100B per seat

### Concurrent Operations

- Thread-safe seat locking
- Atomic booking operations
- Timeout-based seat release

### Scalability

- Singleton pattern for centralized state
- Service layer for business logic separation
- Observer pattern for loose coupling

## 🤝 Contributing

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write descriptive docstrings
- Keep methods focused and small

### Adding Features

1. Create feature branch
2. Implement with tests
3. Update documentation
4. Submit pull request

### Reporting Issues

- Use descriptive issue titles
- Include steps to reproduce
- Provide system information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Design patterns inspired by Gang of Four
- Clean architecture principles
- Python best practices
- Real-world booking system requirements

## 📞 Support

For questions or support:

- Create an issue in the repository
- Check the troubleshooting section
- Review the demo output for examples

---

**Happy Coding! 🎬🎫**
