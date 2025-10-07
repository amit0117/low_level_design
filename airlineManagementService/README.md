# Airline Management Service

A comprehensive airline management system implementation demonstrating various design patterns and architectural principles. This project showcases a complete end-to-end airline management system with flight management, seat booking, payment processing, user management, and real-time notifications.

## 🚀 Features

### Core Functionality

- **User Management** - Complete passenger, staff, and admin profile management
- **Flight Management** - Create, update, and manage flights with aircraft assignment
- **Seat Management** - Dynamic seat allocation with real-time availability tracking
- **Booking Operations** - Search, lock, reserve, and occupy seats with timeout management
- **Payment Processing** - Multiple payment methods for ticket purchases
- **Price Management** - Dynamic pricing with taxes, fees, and discounts using decorator pattern
- **Flight Status Tracking** - Real-time flight status updates with observer notifications
- **Concurrent Access** - Thread-safe operations with seat locking mechanism
- **Comprehensive Reporting** - Detailed airline statistics and analytics

### Design Patterns Implemented

- **Singleton Pattern** - Single instance of AirlineManagement system
- **Observer Pattern** - Real-time notifications for flight status changes
- **State Pattern** - Seat status lifecycle management (Available → Locked → Reserved → Occupied)
- **Strategy Pattern** - Flexible payment processing methods
- **Decorator Pattern** - Dynamic price calculation with taxes and fees
- **Repository Pattern** - Clean data access layer
- **Service Pattern** - Business logic separation
- **Factory Pattern** - User and aircraft creation
- **Facade Pattern** - Simplified interface to complex subsystem

## 📁 Project Structure

```
airlineManagementService/
├── airline_management_demo.py       # Main demo file
├── airline_management.py            # Facade and Singleton implementation
├── app/
│   ├── models/                      # Domain models
│   │   ├── user.py                  # User model with observer implementation
│   │   ├── flight.py                # Flight model with status management
│   │   ├── aircraft.py              # Aircraft model
│   │   ├── seat.py                  # Seat model with state management
│   │   ├── booking.py               # Booking model for reservation operations
│   │   ├── payment_result.py        # Payment result model
│   │   └── enums.py                 # Enums for status and types
│   ├── services/                    # Business logic layer
│   │   ├── payment_service.py       # Payment processing service
│   │   └── booking_service.py       # Booking operations service
│   ├── repositories/                # Data access layer
│   │   ├── flight_repository.py     # Flight data repository
│   │   ├── user_repository.py       # User data repository
│   │   └── booking_repository.py    # Booking data repository
│   ├── observers/                   # Observer pattern implementation
│   │   └── flight_observer.py       # Flight status change observers
│   ├── states/                      # State pattern implementation
│   │   └── seat_state.py            # Seat state management
│   ├── strategies/                  # Strategy pattern implementation
│   │   └── payment_strategy.py      # Payment processing strategies
│   ├── decorators/                  # Decorator pattern implementation
│   │   └── booking_price_decorator.py # Price calculation decorators
│   └── seat_lock_manager.py         # Thread-safe seat locking mechanism
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd airlineManagementService
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt  # If requirements.txt exists
   ```

4. **Run the demo**
   ```bash
   python airline_management_demo.py
   ```

## 🎯 Usage

### Running the Demo

The `airline_management_demo.py` file contains a comprehensive demonstration of all features:

```bash
python airline_management_demo.py
```

### Demo Sections

The demo includes comprehensive sections:

1. **User Management** - Create passengers, staff, and admin users
2. **Aircraft & Flight Creation** - Set up flights with seat allocation
3. **Flight Search** - Search flights by criteria
4. **Booking Workflow** - Complete booking process with payment
5. **Timeout Demonstration** - Automatic seat release after timeout
6. **Multiple Bookings** - Concurrent booking scenarios
7. **Flight Status Updates** - Real-time status changes with notifications
8. **Booking Cancellation** - Cancel and refund operations
9. **Flight Completion** - Complete flight lifecycle
10. **System Statistics** - Comprehensive reporting
11. **Concurrency Testing** - Thread-safe concurrent operations
12. **Seat Status Overview** - Real-time seat availability

### Key Features Demonstrated

- **Thread Safety**: Per-seat locks with timeout management
- **Real-time Notifications**: Observer pattern delivers instant flight status updates
- **Data Consistency**: Thread-safe operations prevent race conditions
- **State Management**: Seat status follows proper state transitions
- **Payment Processing**: Multiple payment methods with strategy pattern
- **Dynamic Pricing**: Decorator pattern for flexible price calculation
- **Error Handling**: Comprehensive validation and error management

## 🔄 Data Flow

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FACADE LAYER                             │
│              AirlineManagement (Singleton)                  │
│         (Simplified interface for all operations)           │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                   SERVICE LAYER                             │
│  PaymentService  │  BookingService  │  (Business Logic)     │
│  (Payment processing, Booking operations)                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                 REPOSITORY LAYER                            │
│ FlightRepository │ UserRepository │ BookingRepository       │
│         (Data Access - Thread-safe operations)              │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                   DOMAIN LAYER                              │
│   Models, States, Strategies, Observers, Decorators         │
│              (Business Entities & Behaviors)                │
└─────────────────────────────────────────────────────────────┘
```

### User Registration Flow

```
User Input → AirlineManagement → UserRepository → User Model
     ↓
Profile Creation → Observer Registration → Notification Setup
```

### Flight Creation Flow

```
Admin Input → AirlineManagement → FlightRepository → Flight Model
     ↓
Aircraft Assignment → Seat Allocation → State Management → Observer Setup
```

### Seat Booking Flow

```
Passenger Request → AirlineManagement → SeatLockManager → Seat State Change
     ↓
Timeout Management → Payment Processing → Booking Creation → Observer Notification
```

### Payment Processing Flow

```
Payment Request → PaymentService → Strategy Pattern → Payment Method
     ↓
Price Calculation → Decorator Pattern → Final Amount → Payment Processing
```

### Flight Status Management Flow

```
Status Change → Flight Model → Observer Pattern → Member Notification
     ↓
Status Update → Flight Repository → Real-time Updates → Passenger Notifications
```

### Seat State Management Flow

```
State Change → SeatState → State Pattern → Observer Notification
     ↓
Status Update → Seat Model → Lock Management → Availability Update
```

### Multi-User Concurrency Flow

```
Multiple Users → ThreadPoolExecutor → Concurrent Booking Operations
     ↓
SeatLockManager → Per-seat Locks → Thread-safe Operations
     ↓
Data Consistency → Observer Notifications → Real-time Updates
```

### Observer Pattern Data Flow

```
Event Trigger (Flight Status Change) → FlightSubject
     ↓
notify_observers() → Observer List → Individual Observer.update()
     ↓
Notification Creation → Passenger Notification → Real-time Display
```

## 🏗️ Architecture

### Design Patterns

#### Singleton Pattern

- `AirlineManagement` ensures single instance
- Thread-safe implementation with double-checked locking
- Centralized access point for all operations

#### Observer Pattern

- Real-time notifications for flight status changes
- Decoupled notification system
- Automatic event propagation to passengers

#### State Pattern

- Seat lifecycle management
- Proper state transitions (Available → Locked → Reserved → Occupied)
- Invalid transition prevention

#### Strategy Pattern

- Flexible payment processing methods
- Easy to add new payment strategies
- Runtime payment method selection

#### Decorator Pattern

- Dynamic price calculation with taxes and fees
- Flexible pricing components
- Easy to add new pricing rules

#### Repository Pattern

- Clean data access layer
- Thread-safe data operations
- Separation of concerns

#### Service Pattern

- Business logic encapsulation
- Input validation and error handling
- Clean API interfaces

#### Factory Pattern

- User and aircraft creation
- Type-specific instantiation
- Extensible user types

#### Facade Pattern

- Simplified interface to complex subsystem
- Hides internal complexity
- Unified API for all operations

### Concurrency & Thread Safety

- **Per-Seat Locks**: Individual locks for each seat
- **Timeout Management**: Automatic seat release after timeout
- **Thread-Safe Repositories**: Process locks for data access operations
- **State Management**: Thread-safe state transitions
- **Observer Notifications**: Thread-safe notification delivery

## 📊 Performance Metrics

The system demonstrates excellent performance characteristics:

- **User Registration**: 7 users in ~0.000 seconds
- **Flight Creation**: 2 flights with 150 seats in ~0.000 seconds
- **Concurrent Bookings**: 8/8 successful with ThreadPoolExecutor
- **Timeout Management**: 2-second automatic cleanup
- **Data Consistency**: Zero data corruption under concurrent access

## 🧪 Testing

The demo includes comprehensive testing covering:

- **Multi-User Concurrency**: ThreadPoolExecutor with 5-8 concurrent operations
- **Data Consistency**: Verification of data integrity under load
- **Observer Pattern**: Real-time notification delivery validation
- **State Management**: Seat state transition testing
- **Error Handling**: Invalid operation testing
- **Performance**: Bulk operation timing
- **Seat Locking**: Timeout and release mechanism testing
- **Payment Processing**: Multiple payment methods validation

## 🔧 Configuration

### Environment Variables

No environment variables required for basic operation.

### Customization

- Payment strategies can be easily extended
- Seat types can be added through enum extension
- New seat states can be implemented
- Additional user profile fields can be added
- Pricing decorators can be customized

## 📈 Scalability

The system is designed for scalability:

- **Horizontal Scaling**: Repository pattern allows database distribution
- **Vertical Scaling**: Efficient algorithms and data structures
- **Caching**: Observer pattern enables efficient notification caching
- **Load Balancing**: Stateless service design supports load balancing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is for educational purposes demonstrating design patterns and architectural principles.

## 🎓 Learning Objectives

This project demonstrates:

- **Design Patterns**: Singleton, Observer, State, Strategy, Decorator, Repository, Service, Factory, Facade
- **Architecture**: Clean separation of concerns, layered architecture
- **Concurrency**: Thread safety, data consistency, race condition prevention
- **Testing**: Comprehensive validation, multi-user scenarios
- **Performance**: Efficient algorithms, scalability considerations
- **Best Practices**: Error handling, validation, documentation

## 🔍 Code Quality

- **Type Hints**: Full type annotation support
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Proper exception management
- **Validation**: Input validation and data integrity checks
- **Thread Safety**: Concurrent access protection
- **Clean Code**: Readable, maintainable, and well-structured

## 🌟 Key Features Showcased

### Real-world Scenarios

- Complete airline workflow from booking to completion
- Comprehensive error handling and validation
- Multi-user concurrent booking simulation
- Performance and scalability testing
- Timeout management for seat reservations

### Design Pattern Integration

- Multiple patterns working together seamlessly
- Clean separation of concerns
- Extensible and maintainable architecture
- Thread-safe concurrent operations
- Real-time notification system

## 🚀 Advanced Features

### Seat Lock Management

- **Per-seat locking**: Individual locks prevent race conditions
- **Timeout mechanism**: Automatic seat release after 2 seconds
- **Thread-safe operations**: Concurrent access protection
- **Atomic operations**: All-or-nothing seat locking

### Dynamic Pricing

- **Base pricing**: Seat type-based pricing
- **Tax calculation**: 18% GST implementation
- **Service charges**: Variable service fees
- **Baggage fees**: Optional baggage charges
- **Airport fees**: Airport-specific charges
- **Discounts**: Passenger type-based discounts

### Flight Status Management

- **Status transitions**: SCHEDULED → BOARDING → DEPARTED → IN_AIR → LANDED → ARRIVED
- **Observer notifications**: Real-time passenger updates
- **State validation**: Proper status transition enforcement

### Concurrency Testing

- **ThreadPoolExecutor**: Concurrent booking simulation
- **Success rate tracking**: Performance metrics
- **Thread safety validation**: Data consistency verification
- **Timeout demonstration**: Automatic cleanup testing

---

**Note**: This is a demonstration project showcasing design patterns and architectural principles. For production use, additional considerations like database persistence, authentication security, API endpoints, and payment gateway integration would be required.
