# Parking Lot System

A comprehensive Parking Lot Management System implementation demonstrating various design patterns and architectural principles. This project showcases a complete parking lot system with multiple floors, different vehicle types, entry/exit gates, ticket generation, payment processing, and concurrent access handling.

## 🚀 Features

### Core Functionality

- **Multiple Floors** - Support for multiple parking levels with flexible spot allocation
- **Different Vehicle Types** - Support for Cars, Motorcycles, and Trucks with type-specific parking spots
- **Entry/Exit Gates** - Multiple entry and exit gates with gate-based processing
- **Ticket Generation** - Automatic ticket generation on vehicle entry with unique ticket IDs
- **Payment Processing** - Multiple payment strategies (Cash, Credit Card, Debit Card, UPI)
- **Pricing Strategies** - Flexible pricing models (Flat Rate, Hourly Rate)
- **Spot Assignment Strategies** - Configurable spot assignment algorithms (Random, Nearest, First Come First Serve, etc.)
- **Real-time Availability** - Real-time parking spot availability tracking
- **Concurrent Access** - Thread-safe operations with fine-grained locking for concurrent vehicle parking/unparking
- **Lock Management** - Hybrid lock management system for optimal concurrency

### Design Patterns Implemented

- **Singleton Pattern** - ParkingLot, TicketRepository, GateRepository singleton instances (ensures single instance per service)
- **Strategy Pattern** - Parking spot assignment strategies, Payment strategies, Pricing strategies (interchangeable algorithms)
- **Repository Pattern** - Ticket and Gate repositories for centralized data management (Singleton pattern)
- **Template Method Pattern** - Gate processing flow (Entry: allocate spot → create ticket → park vehicle | Exit: get ticket → process payment → unpark vehicle)

### Domain Entities

| Domain Area        | Key Entities                                                                                                                                                                     |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Parking System** | `ParkingLot`, `Floor`, `ParkingSpot`, `Gate` (EntryGate, ExitGate)                                                                                                               |
| **Vehicles**       | `Vehicle`, `Car`, `Motorcycle`, `Truck`                                                                                                                                          |
| **Transactions**   | `Ticket`, `PaymentResponse`                                                                                                                                                      |
| **Strategies**     | `ParkingSpotAssignmentStrategy`, `RandomSpotAssignmentStrategy`, `PaymentStrategy`, `CashPaymentStrategy`, `PricingStrategy`, `FlatRatePricingStrategy`, `HourlyPricingStrategy` |
| **Repositories**   | `TicketRepository`, `GateRepository`                                                                                                                                             |
| **Concurrency**    | `LockManager` (hybrid lock management for parking spots)                                                                                                                         |
| **Enums**          | `VehicleType`, `ParkingSpotStatus`, `PaymentStatus`, `PaymentMethod`, `ParkingTicketStatus`, `GateType`                                                                          |

### Core Entities Overview

#### Parking System Domain

- **ParkingLot**: Main parking lot singleton with floor management, gate management, ticket management, and strategy delegation
- **Floor**: Represents a parking floor with multiple parking spots and lock management
- **ParkingSpot**: Individual parking spot with vehicle type compatibility, status (Available/Occupied), and vehicle reference
- **Gate**: Base class for EntryGate and ExitGate with gate-based processing
  - **EntryGate**: Processes vehicle entry, allocates parking spot, creates ticket
  - **ExitGate**: Processes vehicle exit, handles payment, releases parking spot

#### Vehicle Domain

- **Vehicle**: Base vehicle class with license plate and vehicle type
- **Car**: Car vehicle type (VehicleType.CAR)
- **Motorcycle**: Motorcycle vehicle type (VehicleType.MOTORCYCLE)
- **Truck**: Truck vehicle type (VehicleType.TRUCK)

#### Transaction Domain

- **Ticket**: Parking ticket with vehicle info, parking spot, entry/exit gates, floor number, timestamps, and status
- **PaymentResponse**: Payment result with amount, payment method, and payment status

#### Strategy Domain

- **ParkingSpotAssignmentStrategy**: Abstract strategy for parking spot assignment
  - **RandomSpotAssignmentStrategy**: Assigns random available spot (current implementation)
  - Can be extended: NearestSpotAssignmentStrategy, FirstComeFirstServeStrategy, ZoneBasedStrategy, PreferredSpotStrategy
- **PaymentStrategy**: Abstract strategy for payment processing
  - **CashPaymentStrategy**: Cash payment implementation (current implementation)
  - Can be extended: CreditCardPaymentStrategy, DebitCardPaymentStrategy, UPIPaymentStrategy
- **PricingStrategy**: Abstract strategy for pricing calculation
  - **FlatRatePricingStrategy**: Fixed rate pricing (current implementation)
  - **HourlyPricingStrategy**: Time-based pricing (hourly rate)

#### Repository Domain

- **TicketRepository**: Manages all parking tickets (Singleton)
- **GateRepository**: Manages all entry and exit gates (Singleton)

#### Concurrency Domain

- **LockManager**: Hybrid lock management system for parking spots
  - Per-floor lock management (not global)
  - Lazy lock creation (on-demand)
  - Fine-grained locking for optimal concurrency
  - Prevents race conditions in concurrent parking/unparking operations

## 📁 Project Structure

```
parkingLot/
├── parking_lot.py              # Main ParkingLot singleton class
├── demo.py                      # Comprehensive demo with all test scenarios
├── app/
│   ├── models/                  # Domain models
│   │   ├── floor.py             # Floor model with parking spots and lock management
│   │   ├── parking_spot.py      # ParkingSpot model (status, vehicle type, vehicle reference)
│   │   ├── vehicle.py           # Vehicle models (Vehicle, Car, Motorcycle, Truck)
│   │   ├── gate.py              # Gate models (Gate, EntryGate, ExitGate)
│   │   ├── ticket.py            # Ticket model with timestamps and status
│   │   ├── payment_response.py  # PaymentResponse model
│   │   └── enums.py              # Enum definitions (VehicleType, ParkingSpotStatus, PaymentStatus, etc.)
│   ├── repositories/            # Repository pattern implementation
│   │   ├── ticket_repository.py # Ticket repository (Singleton)
│   │   └── gate_repository.py    # Gate repository (Singleton)
│   ├── strategies/              # Strategy pattern implementation
│   │   ├── parking_spot_assignment_strategy.py  # Spot assignment strategies
│   │   ├── payment_strategy.py                  # Payment processing strategies
│   │   └── pricing_strategy.py                  # Pricing calculation strategies
│   └── lock_manager.py          # Hybrid lock management for concurrent access
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Setup Instructions

1. **Navigate to the Parking Lot directory**

   ```bash
   cd low_level_design/parkingLot
   ```

2. **Create and activate virtual environment** (optional but recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Run the demo**

   ```bash
   python demo.py
   ```

## 🎯 Usage

### Running the Demo

The `demo.py` file contains a comprehensive demonstration of all features:

```bash
python demo.py
```

### Demo Sections

The demo includes the following test scenarios:

#### 1. Setup Parking Lot

- Creates multiple floors (Floor 1, 2, 3)
- Adds parking spots for different vehicle types:
  - Floor 1: 5 Car spots + 5 Motorcycle spots
  - Floor 2: 5 Car spots + 5 Truck spots
  - Floor 3: 3 Motorcycle spots + 3 Car spots
- Creates multiple entry gates (Gate 1, Gate 2)
- Creates multiple exit gates (Gate 1, Gate 2)

#### 2. Concurrent Parking Access

- Tests simultaneous vehicle parking using multiple threads
- 10 vehicles attempt to park concurrently (6 Cars, 2 Motorcycles, 2 Trucks)
- Demonstrates thread-safe spot allocation
- Shows proper spot assignment based on vehicle type
- Verifies no duplicate spot assignments

#### 3. Vehicle Exit and Payment

- Tests vehicle exit through exit gates
- Processes payment for parking duration
- Releases parking spots after payment
- Updates parking spot availability
- Verifies spot release after unparking

#### 4. No Spots Available Scenario

- Tests parking when all spots are filled
- Attempts to park vehicles when no spots available
- Properly handles and reports unavailability
- Demonstrates graceful handling of capacity limits

#### 5. Mixed Vehicle Types

- Tests parking different vehicle types simultaneously
- Verifies spot assignment based on vehicle type compatibility
- Shows proper separation of vehicle types across floors

#### 6. Concurrent Booking Same Spots

- Tests high-concurrency scenario with limited spots
- Multiple vehicles attempt to park when spots are almost full
- Demonstrates thread safety in race condition scenarios
- Verifies no spot double-booking

### Key Features Demonstrated

- **Singleton Pattern**: Single ParkingLot instance across the application
- **Strategy Pattern**: Interchangeable spot assignment, payment, and pricing strategies
- **Repository Pattern**: Centralized ticket and gate management
- **Thread Safety**: Concurrent parking/unparking operations
- **Lock Management**: Fine-grained locking with LockManager
- **Error Handling**: Proper handling when spots are unavailable
- **Multiple Gates**: Entry and exit through different gates

## 📊 Entity Relationship Diagram

### Core Entities and Relationships

```
┌─────────────────────────────────────┐
│          ParkingLot                 │
│─────────────────────────────────────│
│ id                                  │
│ floors (List<Floor>)                │
│ entry_gates (List<EntryGate>)       │
│ exit_gates (List<ExitGate>)         │
│ spot_assignment_strategy            │
│ payment_strategy                    │
│ pricing_strategy                    │
└──────┬──────────────────────────────┘
       │
       │ 1..* (contains)
       │
       ▼
┌─────────────────────────────────────┐
│            Floor                    │
│─────────────────────────────────────│
│ floor_number                        │
│ parking_spots (List<ParkingSpot>)   │
│ lock_manager (LockManager)          │
└──────┬──────────────────────────────┘
       │
       │ 1..* (contains)
       │
       ▼
┌─────────────────────────────────────┐
│         ParkingSpot                 │
│─────────────────────────────────────│
│ spot_number                         │
│ vehicle_type (VehicleType)          │
│ status (ParkingSpotStatus)          │
│ vehicle (Vehicle)                   │
└──────┬──────────────────────────────┘
       │
       │ 0..1 (parked in)
       │
       ▼
┌─────────────────────────────────────┐
│           Vehicle                   │
│─────────────────────────────────────│
│ license_plate                       │
│ vehicle_type (VehicleType)          │
└─────────────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│   Car    │  │Motorcycle│  │  Truck   │
└──────────┘  └──────────┘  └──────────┘

┌─────────────────────────────────────┐
│            Ticket                   │
│─────────────────────────────────────│
│ ticket_id                           │
│ vehicle (Vehicle)                   │
│ parking_spot (ParkingSpot)          │
│ status (ParkingTicketStatus)        │
│ start_time                          │
│ end_time                            │
│ entry_gate_number                   │
│ exit_gate_number                    │
│ floor_number                        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│             Gate                    │
│─────────────────────────────────────│
│ gate_number                         │
│ gate_type (GateType)                │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┐
       ▼              ▼
┌─────────────┐  ┌─────────────┐
│ EntryGate   │  │  ExitGate   │
└─────────────┘  └─────────────┘

┌─────────────────────────────────────┐
│      PaymentResponse                │
│─────────────────────────────────────│
│ amount                              │
│ payment_method (PaymentMethod)      │
│ payment_status (PaymentStatus)      │
└─────────────────────────────────────┘
```

### Entity Relationships

1. **ParkingLot ↔ Floor** (One-to-Many)

   - A ParkingLot has multiple Floors
   - Each Floor belongs to one ParkingLot

2. **Floor ↔ ParkingSpot** (One-to-Many)

   - A Floor has multiple ParkingSpots
   - Each ParkingSpot belongs to one Floor

3. **ParkingSpot ↔ Vehicle** (One-to-One, Optional)

   - A ParkingSpot can have one Vehicle parked (when OCCUPIED)
   - A Vehicle can be parked in one ParkingSpot
   - Relationship is optional (spot can be AVAILABLE)

4. **Vehicle Inheritance Hierarchy**

   - `Vehicle` (base class)
   - `Car`, `Motorcycle`, `Truck` (subclasses)
   - Each vehicle type has specific parking requirements

5. **Ticket ↔ Vehicle** (One-to-One)

   - A Ticket is created for one Vehicle
   - A Vehicle can have one active Ticket

6. **Ticket ↔ ParkingSpot** (One-to-One)

   - A Ticket references one ParkingSpot
   - A ParkingSpot can be referenced by one active Ticket

7. **Ticket ↔ Gate** (Many-to-One)

   - A Ticket has one entry_gate_number
   - A Ticket has one exit_gate_number
   - Multiple Tickets can use the same Gate

8. **Gate Inheritance Hierarchy**

   - `Gate` (base class)
   - `EntryGate`, `ExitGate` (subclasses)
   - Different processing logic for entry vs exit

9. **Strategy Pattern Relationships**

   - ParkingLot uses `ParkingSpotAssignmentStrategy` (delegates spot selection)
   - ParkingLot uses `PaymentStrategy` (delegates payment processing)
   - ParkingLot uses `PricingStrategy` (delegates price calculation)

10. **Repository Pattern Relationships**
    - `TicketRepository` manages all Tickets (Singleton)
    - `GateRepository` manages all Gates (Singleton)

## 🔄 Data Flow

### System Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│              PARKING LOT LAYER                               │
│              ParkingLot (Singleton)                          │
│    (Floor management, Gate management, Strategy delegation)  │
└────────────────────┬─────────────────────────────────────────┘
                     │
┌────────────────────┴─────────────────────────────────────────┐
│              REPOSITORY LAYER                                │
│         TicketRepository │ GateRepository                    │
│         (Singleton instances)                                │
└────────────────────┬─────────────────────────────────────────┘
                     │
┌────────────────────┴─────────────────────────────────────────┐
│              STRATEGY LAYER                                  │
│  ParkingSpotAssignmentStrategy │ PaymentStrategy             │
│  PricingStrategy                                             │
└────────────────────┬─────────────────────────────────────────┘
                     │
┌────────────────────┴─────────────────────────────────────────┐
│              FLOOR & SPOT LAYER                              │
│         Floor (with LockManager)                             │
│         ParkingSpot (per-spot locking)                       │
└────────────────────┬─────────────────────────────────────────┘
                     │
┌────────────────────┴─────────────────────────────────────────┐
│              GATE LAYER                                      │
│         EntryGate │ ExitGate                                 │
│    (Entry: allocate → ticket → park)                         │
│    (Exit: ticket → payment → unpark)                         │
└──────────────────────────────────────────────────────────────┘
```

### Vehicle Entry Flow

```
Vehicle arrives → EntryGate.process_entry()
     ↓
ParkingLot.allocate_parking_spot()
     ↓
ParkingSpotAssignmentStrategy.assign_parking_spot()
     ↓
Find available spot → Select floor and spot
     ↓
ParkingLot.create_ticket()
     ↓
TicketRepository.create_ticket()
     ↓
Floor.park_vehicle() [with LockManager.acquire()]
     ↓
ParkingSpot.park_vehicle() → Mark spot as OCCUPIED
     ↓
Return Ticket to vehicle
```

### Vehicle Exit Flow

```
Vehicle arrives at exit → ExitGate.process_exit(ticket_id)
     ↓
GateRepository.get_exit_gate()
     ↓
TicketRepository.get_ticket(ticket_id)
     ↓
ParkingLot.process_payment()
     ↓
PricingStrategy.calculate_price() → Get parking duration → Calculate price
     ↓
PaymentStrategy.pay() → Process payment
     ↓
Ticket.update_end_time() → Update status to PAID
     ↓
Floor.unpark_vehicle() [with LockManager.acquire()]
     ↓
ParkingSpot.unpark_vehicle() → Mark spot as AVAILABLE
     ↓
Return PaymentResponse
```

### Spot Assignment Flow

```
Vehicle arrives → get_vehicle_type()
     ↓
ParkingLot.get_all_available_parking_spots(vehicle_type)
     ↓
For each floor:
  Floor.get_available_parking_spots(vehicle_type)
     ↓
Filter spots: is_available() && matches vehicle_type
     ↓
ParkingSpotAssignmentStrategy.assign_parking_spot()
     ↓
Return (floor_number, parking_spot)
```

### Concurrent Access Flow

```
Multiple threads attempt to park
     ↓
Each thread calls EntryGate.process_entry()
     ↓
ParkingLot.allocate_parking_spot()
     ↓
Floor.park_vehicle(spot_number)
     ↓
LockManager.acquire(spot_number)
     ↓
Lock created/retrieved for spot (lazy creation)
     ↓
Acquire lock → Check availability → Park vehicle
     ↓
Release lock → Other threads can proceed
     ↓
No duplicate assignments (thread-safe)
```

## 🏗️ Architecture

### Design Patterns

#### Singleton Pattern

The `ParkingLot`, `TicketRepository`, and `GateRepository` classes ensure single instances:

```python
class ParkingLot:
    _lock = Lock()
    _instance: "ParkingLot" = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

**Benefits**:

- Single parking lot instance across the application
- Thread-safe implementation with double-checked locking
- Centralized access point for all parking operations
- Prevents multiple parking lot instances from conflicting

**Use Case**: Ensures that only one parking lot instance exists, maintaining consistency in floor management, gate management, and ticket handling.

#### Strategy Pattern

The system uses Strategy pattern for three key algorithms:

1. **ParkingSpotAssignmentStrategy**: How to assign spots

   - `RandomSpotAssignmentStrategy`: Random assignment
   - Can extend: NearestSpotAssignmentStrategy, FirstComeFirstServeStrategy, ZoneBasedStrategy

2. **PaymentStrategy**: How to process payments

   - `CashPaymentStrategy`: Cash payment
   - Can extend: CreditCardPaymentStrategy, DebitCardPaymentStrategy, UPIPaymentStrategy

3. **PricingStrategy**: How to calculate prices
   - `FlatRatePricingStrategy`: Fixed rate
   - `HourlyPricingStrategy`: Time-based pricing
   - Can extend: PeakHourPricingStrategy, VIPPricingStrategy

```python
class ParkingLot:
    def __init__(self):
        self.parking_spot_assignment_strategy = RandomSpotAssignmentStrategy()
        self.payment_strategy = CashPaymentStrategy()
        self.pricing_strategy = FlatRatePricingStrategy()

    def allocate_parking_spot(self, vehicle: Vehicle):
        # Uses current strategy
        return self.parking_spot_assignment_strategy.assign_parking_spot(...)
```

**Benefits**:

- Easy to switch algorithms at runtime
- Extensible without modifying existing code
- Follows Open/Closed Principle
- Clean separation of concerns

#### Repository Pattern

Repositories manage domain objects:

- **TicketRepository**: Manages all parking tickets (Singleton)
- **GateRepository**: Manages all entry and exit gates (Singleton)

```python
class TicketRepository:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def create_ticket(self, vehicle, parking_spot, entry_gate, floor):
        ticket = Ticket(vehicle, parking_spot, entry_gate, floor)
        self.tickets[ticket.get_ticket_id()] = ticket
        return ticket
```

**Benefits**:

- Centralized data management
- Single source of truth
- Easy to swap implementations (e.g., database-backed)
- Clean API for data access

#### Template Method Pattern

Gates follow a consistent processing flow:

**EntryGate Template**:

1. Allocate parking spot
2. Create ticket
3. Park vehicle
4. Return ticket

**ExitGate Template**:

1. Get ticket
2. Calculate price
3. Process payment
4. Update ticket
5. Unpark vehicle
6. Return payment response

```python
class EntryGate(Gate):
    def process_entry(self, vehicle: Vehicle) -> Ticket:
        # Template method flow
        floor_number, parking_spot = parking_lot.allocate_parking_spot(vehicle)
        ticket = parking_lot.create_ticket(vehicle, parking_spot, ...)
        floor = parking_lot.get_floor(floor_number)
        floor.park_vehicle(parking_spot.get_spot_number(), vehicle)
        return ticket
```

**Benefits**:

- Consistent processing flow
- Easy to extend with new gate types
- Centralized error handling
- Follows DRY principle

### Lock Management Architecture

The system uses a hybrid lock management approach:

#### Problem Statement

1. **Global Lock**: Too coarse-grained, poor concurrency
2. **Per-Spot Lock**: Too many locks, memory overhead
3. **Per-Floor Lock**: Better balance, but still limits concurrency

#### Solution: Hybrid LockManager

```python
class LockManager:
    def __init__(self):
        self.spot_locks: dict[int, Lock] = defaultdict(Lock)
        self._manager_lock = Lock()

    @contextmanager
    def acquire(self, spot_id: int):
        lock = self.get_lock(spot_id)
        lock.acquire()
        try:
            yield
        finally:
            lock.release()
```

**Features**:

- **Per-Floor Scoped**: Each Floor has its own LockManager
- **Lazy Creation**: Locks created on-demand (not pre-allocated)
- **Fine-Grained**: Per-spot locking for maximum concurrency
- **Thread-Safe**: Manager lock prevents race conditions in lock creation

**Benefits**:

- Optimal concurrency: Multiple vehicles can park on different floors/spots simultaneously
- Memory Efficient: Only creates locks for spots that are accessed
- Scalable: Can scale to thousands of spots per floor
- Distributed-Ready: Can be replaced with Redis/ZooKeeper for distributed systems

### Use Cases for Design Patterns

#### Singleton Pattern

- **Single Parking Lot**: Ensures only one parking lot instance exists
- **Centralized Management**: All parking operations go through single instance
- **Resource Efficiency**: Prevents duplicate repositories and resource allocation
- **Thread Safety**: Safe concurrent access with double-checked locking

#### Strategy Pattern

- **Spot Assignment**: Easy to switch between assignment algorithms
- **Payment Methods**: Support multiple payment methods (Cash, Card, UPI)
- **Pricing Models**: Support different pricing strategies (Flat, Hourly, Peak)

#### Repository Pattern

- **Ticket Management**: Centralized ticket storage and retrieval
- **Gate Management**: Centralized gate registration and access
- **Future Extensibility**: Easy to swap with database-backed repositories

#### Template Method Pattern

- **Gate Processing**: Consistent entry/exit processing flow
- **Extensibility**: Easy to add new gate types (VIP Gate, Emergency Gate)
- **Error Handling**: Centralized error handling and rollback

## 🧪 Testing

The demo includes comprehensive testing covering:

- **Basic Setup**: Floor and spot creation
- **Concurrent Parking**: Multiple vehicles parking simultaneously
- **Vehicle Exit**: Payment processing and spot release
- **No Spots Available**: Handling when parking lot is full
- **Mixed Vehicle Types**: Different vehicle types parking together
- **Concurrent Booking**: High-concurrency scenarios with limited spots
- **Thread Safety**: Concurrent access validation
- **Spot Assignment**: Proper spot assignment based on vehicle type
- **Payment Processing**: Payment calculation and processing

### Test Scenarios

1. **Setup**: Creates 3 floors with different vehicle type spots
2. **Concurrent Parking**: 10 vehicles parking simultaneously through different gates
3. **Vehicle Exit**: Multiple vehicles exiting with payment processing
4. **Capacity Testing**: Fills all spots and tests rejection
5. **Mixed Vehicle Types**: Cars, Motorcycles, and Trucks parking together
6. **Concurrent Booking**: Multiple threads attempting to book same spots
7. **Availability Tracking**: Real-time spot availability updates

## 🔧 Configuration

### Environment Variables

No environment variables required for basic operation.

### Customization

- **Add New Spot Assignment Strategy**: Implement `ParkingSpotAssignmentStrategy` and set in ParkingLot
- **Add New Payment Method**: Implement `PaymentStrategy` and set in ParkingLot
- **Add New Pricing Model**: Implement `PricingStrategy` and set in ParkingLot
- **Modify Floor Structure**: Add floors with different spot configurations
- **Add New Vehicle Types**: Extend `VehicleType` enum and create vehicle classes

## 📈 Scalability

The system is designed for scalability:

- **Horizontal Scaling**: Repository pattern allows multiple parking lot instances
- **Vertical Scaling**: Efficient algorithms and data structures
- **Thread Safety**: Concurrent vehicle handling with fine-grained locks
- **Lock Management**: Hybrid approach scales to thousands of spots
- **Strategy Pattern**: Easy to add new algorithms without code changes
- **Distributed-Ready**: LockManager can be replaced with distributed lock service (Redis/ZooKeeper)

## 🎓 Learning Objectives

This project demonstrates:

- **Design Patterns**: Singleton, Strategy, Repository, Template Method
- **Architecture**: Clean separation of concerns, layered architecture
- **Concurrency**: Thread safety, fine-grained locking, race condition prevention
- **Domain Modeling**: Parking lot domain with entities and relationships
- **Error Handling**: Comprehensive validation and error management
- **Scalability**: Lock management, efficient algorithms
- **Extensibility**: Strategy pattern for easy algorithm swapping

## 🔍 Code Quality

- **Type Hints**: Full type annotation support
- **Error Handling**: Proper exception management
- **Validation**: Input validation and data integrity checks
- **Thread Safety**: Concurrent access protection with LockManager
- **Clean Code**: Readable, maintainable, and well-structured
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion

## 📊 Performance Metrics

The system demonstrates excellent performance characteristics:

- **Concurrent Operations**: Thread-safe concurrent parking/unparking
- **Lock Overhead**: Minimal lock contention with hybrid approach
- **Memory Efficiency**: Lazy lock creation reduces memory footprint
- **Spot Assignment**: Fast spot allocation with strategy pattern
- **Payment Processing**: Efficient payment calculation and processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is for educational purposes demonstrating design patterns and architectural principles.

---

**Note**: This is a demonstration project showcasing design patterns and architectural principles. For production use, additional considerations like database persistence, network security, encryption, and real hardware integration would be required.
