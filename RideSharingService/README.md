# 🚗 Ride Sharing Service - Low Level Design

A comprehensive ride-sharing service implementation showcasing multiple design patterns and real-world scenarios.

## 📋 Table of Contents

- [Overview](#overview)
- [Design Patterns Implemented](#design-patterns-implemented)
- [Project Structure](#project-structure)
- [Features](#features)
- [Getting Started](#getting-started)
- [Demo Scenarios](#demo-scenarios)
- [API Documentation](#api-documentation)
- [Business Logic](#business-logic)
- [Edge Cases Handled](#edge-cases-handled)
- [Contributing](#contributing)

## 🎯 Overview

This project implements a complete ride-sharing service similar to Uber/Ola, demonstrating various design patterns and handling real-world scenarios. The system supports multiple vehicle types, dynamic pricing, driver matching strategies, and comprehensive ride lifecycle management.

## 🏗️ Design Patterns Implemented

### 1. **Singleton Pattern**

- `RideSharingSystem` ensures only one instance exists
- Thread-safe implementation with double-checked locking
- Centralized system management

### 2. **Factory Pattern**

- `VehicleFactory` creates different vehicle types (Auto, Sedan, SUV, Luxury)
- Abstract factory pattern for extensible vehicle creation
- Type-safe vehicle instantiation

### 3. **Strategy Pattern**

- `DriverMatchingStrategy` for flexible driver selection algorithms
- `PricingStrategy` for different fare calculation methods
- Runtime strategy switching capability

### 4. **Decorator Pattern**

- `PricingDecorator` for adding pricing modifiers
- Supports discounts, surge pricing, and taxes
- Composable pricing components

### 5. **Observer Pattern**

- `RideObserver` for real-time ride status notifications
- Automatic notifications to drivers and riders
- Loose coupling between components

### 6. **State Pattern**

- `RideState` manages ride lifecycle states
- States: REQUESTED → ACCEPTED → IN_PROGRESS → COMPLETED/CANCELLED
- Encapsulated state-specific behavior

## 📁 Project Structure

```
RideSharingService/
├── app/
│   ├── decorators/
│   │   └── pricing_decorator.py      # Pricing modifiers (discount, surge, tax)
│   ├── models/
│   │   ├── driver.py                 # Driver entity with vehicle and earnings
│   │   ├── enums.py                  # All system enums
│   │   ├── location.py               # Location/coordinate handling
│   │   ├── payment_result.py         # Payment transaction details
│   │   ├── ride.py                   # Core ride entity
│   │   ├── ride_state.py             # Ride state management
│   │   ├── rider.py                  # Rider entity
│   │   ├── user.py                   # Base user class
│   │   ├── vehicle.py                # Vehicle entity
│   │   └── vehicle_factory.py        # Vehicle creation factories
│   ├── observers/
│   │   └── ride_observer.py          # Observer pattern implementation
│   ├── services/
│   │   ├── payment_service.py        # Payment processing
│   │   ├── ride_service.py           # Ride management
│   │   └── user_service.py           # User management
│   └── strategies/
│       ├── driver_matching_strategy.py  # Driver selection algorithms
│       ├── payment_strategy.py           # Payment processing strategies
│       └── pricing_strategy.py          # Fare calculation strategies
├── ride_sharing_system.py            # Main system orchestrator
└── run.py                            # Comprehensive demo
```

## 📊 Entity Relationship Diagram

### Core Entities and Relationships

```
┌─────────────────────────────────────┐
│    RideSharingSystem                │
│─────────────────────────────────────│
│ (Singleton)                         │
│ - ride_service                      │
│ - payment_service                   │
│ - user_service                      │
│ - driver_matching_strategy          │
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
│ contact                             │
│ type (UserType)                     │
│ ride_history (List<Ride>)           │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┐
       ▼              ▼
┌─────────────┐ ┌─────────────┐
│   Rider     │ │   Driver    │
│             │ │  - vehicle  │
│             │ │  - location │
│             │ │  - status   │
│             │ │  - earnings │
└─────────────┘ └─────────────┘

┌─────────────────────────────────────┐
│            Ride                     │
│─────────────────────────────────────│
│ id                                  │
│ rider (Rider)                       │
│ driver (Driver)                     │
│ pickup (Location)                   │
│ destination (Location)              │
│ state (RideState)                   │
│ status (RideStatus)                 │
│ payment (PaymentResult)             │
│ observers (List<Observer>)          │
└──────┬──────────────────────────────┘
       │
       │ references
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌──────────────┐
│  Location   │ │  Vehicle    │ │ PaymentResult│
└─────────────┘ └─────────────┘ └──────────────┘

┌─────────────────────────────────────┐
│           Vehicle                   │
│─────────────────────────────────────│
│ id                                  │
│ license_plate                       │
│ vehicle_type (VehicleType)          │
│ model                               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│          Location                   │
│─────────────────────────────────────│
│ latitude                            │
│ longitude                           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│        RideState                    │
│─────────────────────────────────────│
│ (Abstract)                          │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┬──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Requested   │ │  Accepted   │ │ InProgress  │ │  Completed  │ │  Cancelled  │
│   State     │ │   State     │ │   State     │ │   State     │ │   State     │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘

┌─────────────────────────────────────┐
│    DriverMatchingStrategy           │
│─────────────────────────────────────│
│ (Abstract)                          │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ▼
┌─────────────┐
│  Nearest    │
│  Driver     │
│  Matching   │
└─────────────┘

┌─────────────────────────────────────┐
│      PricingStrategy                │
│─────────────────────────────────────│
│ (Abstract)                          │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┐
       ▼              ▼
┌─────────────┐ ┌─────────────┐
│ Distance    │ │  Vehicle    │
│  Based      │ │   Based     │
└─────────────┘ └─────────────┘
```

### Entity Relationships

1. **RideSharingSystem ↔ User** (One-to-Many)

   - System manages multiple Users
   - Users stored in UserService

2. **User Inheritance Hierarchy**

   - `User` (base class)
   - `Rider`, `Driver` (subclasses)

3. **Rider ↔ Ride** (One-to-Many)

   - A Rider can request multiple Rides
   - Each Ride has one Rider

4. **Driver ↔ Ride** (One-to-Many)

   - A Driver can accept multiple Rides
   - Each Ride has one Driver (when accepted)

5. **Driver ↔ Vehicle** (One-to-One)

   - A Driver has one Vehicle
   - A Vehicle belongs to one Driver

6. **Driver ↔ Location** (One-to-One)

   - A Driver has one current Location
   - Location updated as driver moves

7. **Ride ↔ Location** (Many-to-One, Two references)

   - A Ride has one pickup Location
   - A Ride has one destination Location

8. **Ride ↔ Vehicle** (Many-to-One, via Driver)

   - A Ride uses one Vehicle (through driver)
   - A Vehicle can be used in multiple Rides

9. **Ride ↔ PaymentResult** (One-to-One)

   - A Ride has one PaymentResult
   - PaymentResult created when ride completes

10. **Ride ↔ RideState** (One-to-One)

    - Each Ride has one current State
    - State transitions: Requested → Accepted → InProgress → Completed/Cancelled

11. **RideSharingSystem ↔ DriverMatchingStrategy** (One-to-One)

    - System uses one MatchingStrategy
    - Strategy selects which driver handles a ride

12. **Ride ↔ PricingStrategy** (One-to-One, via decorators)

    - Ride uses PricingStrategy for fare calculation
    - Decorators add modifiers (discount, surge, tax)

13. **Observer Pattern Relationships**
    - Ride implements `RideSubject` - notifies on status changes
    - Rider and Driver implement `RideObserver` - receive notifications

## 🔄 Data Flow Diagrams

### 1. Ride Request Flow

```
┌──────────┐
│  Rider   │
└────┬─────┘
     │
     │ 1. request_ride(pickup, destination, type)
     ▼
┌─────────────────┐
│RideSharingSystem│
└────┬────────────┘
     │
     │ 2. ride_service.request_ride()
     ▼
┌─────────────────┐
│  RideService    │
└────┬────────────┘
     │
     │ 3. Find driver (using strategy)
     ▼
┌─────────────────┐
│MatchingStrategy │
└────┬────────────┘
     │
     │ 4. Calculate fare
     ▼
┌─────────────────┐
│ PricingStrategy │
│  + Decorators   │
└────┬────────────┘
     │
     │ 5. Create Ride
     │ 6. Set state to Requested
     ▼
┌─────────────────┐
│     Ride        │
└────┬────────────┘
     │
     │ 7. notify_observers()
     ▼
┌─────────────────┐
│   Driver        │
│  (Notified)     │
└─────────────────┘
```

### 2. Ride Acceptance Flow

```
┌──────────┐
│  Driver  │
└────┬─────┘
     │
     │ 1. accept_ride(ride_id)
     ▼
┌─────────────────┐
│RideSharingSystem│
└────┬────────────┘
     │
     │ 2. ride_service.accept_ride()
     ▼
┌─────────────────┐
│  RideService    │
└────┬────────────┘
     │
     │ 3. ride.accept_ride(driver)
     ▼
┌─────────────────┐
│     Ride        │
└────┬────────────┘
     │
     │ 4. state.accept_ride()
     │ 5. Update state to Accepted
     │ 6. notify_observers()
     ▼
┌─────────────────┐
│  Rider & Driver │
│  (Notified)     │
└─────────────────┘
```

### 3. Ride Completion Flow

```
┌──────────┐
│  Driver  │
└────┬─────┘
     │
     │ 1. complete_ride(ride_id)
     ▼
┌─────────────────┐
│RideSharingSystem│
└────┬────────────┘
     │
     │ 2. ride_service.complete_ride()
     ▼
┌─────────────────┐
│  RideService    │
└────┬────────────┘
     │
     │ 3. Calculate final fare
     │ 4. Process payment
     ▼
┌─────────────────┐
│ PaymentService  │
└────┬────────────┘
     │
     │ 5. ride.complete_ride()
     │ 6. Update state to Completed
     │ 7. Update driver earnings
     │ 8. notify_observers()
     ▼
┌─────────────────┐
│  Rider & Driver │
│  (Notified)     │
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
│    RideSharingSystem                │
│    (Singleton)                      │
│  - Ride Management                  │
│  - User Management                  │
│  - Payment Processing               │
└──────┬──────────────────────────────┘
       │
       ├──────────────────┬──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ RideService │  │UserService  │  │ Payment    │
│             │  │             │  │ Service    │
└─────────────┘  └─────────────┘  └─────────────┘
       │                  │                  │
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Rides     │  │   Users     │  │  Payments   │
│  - Riders   │  │  - Riders   │  │             │
│  - Drivers  │  │  - Drivers  │  │             │
│  - Vehicles │  │             │  │             │
└─────────────┘  └─────────────┘  └─────────────┘
       │
       │
       ▼
┌─────────────────────────────────────┐
│         Pattern Layer               │
│  - RideState (State)                │
│  - DriverMatchingStrategy           │
│  - PricingStrategy                  │
│  - PricingDecorator                 │
└─────────────────────────────────────┘
```

## 📋 Entity Attributes Summary

### User Entity

- `id`: Unique identifier (UUID)
- `name`: User's name
- `contact`: Contact information
- `type`: UserType (RIDER, DRIVER)
- `ride_history`: List of Ride objects

### Rider Entity (extends User)

- Inherits all User attributes
- Implements RideObserver interface

### Driver Entity (extends User)

- `vehicle`: Reference to Vehicle
- `location`: Current Location
- `status`: DriverStatus (ONLINE, OFFLINE, BUSY)
- `total_earnings`: Total earnings from rides
- Implements RideObserver interface

### Ride Entity

- `id`: Unique identifier (UUID)
- `rider`: Reference to Rider
- `driver`: Reference to Driver (optional initially)
- `pickup`: Pickup Location
- `destination`: Destination Location
- `state`: RideState object
- `status`: RideStatus (REQUESTED, ACCEPTED, IN_PROGRESS, COMPLETED, CANCELLED)
- `payment`: PaymentResult object
- `observers`: List of Observer objects

### Vehicle Entity

- `id`: Unique identifier (UUID)
- `license_plate`: Vehicle license plate
- `vehicle_type`: VehicleType (AUTO, SEDAN, SUV, LUXURY)
- `model`: Vehicle model name

### Location Entity

- `latitude`: Latitude coordinate
- `longitude`: Longitude coordinate

### PaymentResult Entity

- `amount`: Payment amount
- `payment_method`: PaymentMethod
- `payment_status`: PaymentStatus

## ✨ Features

### Core Features

- **Multi-vehicle Support**: Auto, Sedan, SUV, Luxury vehicles
- **Dynamic Pricing**: Distance-based, vehicle-based, and decorator-enhanced pricing
- **Driver Matching**: Nearest driver algorithm with configurable distance
- **Ride Lifecycle**: Complete ride state management
- **Real-time Notifications**: Observer-based status updates
- **Earnings Tracking**: Driver earnings and ride history
- **Payment Processing**: Multiple payment methods support

### Advanced Features

- **Surge Pricing**: Dynamic pricing during high demand
- **Discount System**: Coupon and promotional pricing
- **Tax Calculation**: Automatic tax computation
- **Driver Status Management**: Online/Offline/Busy states
- **Ride Cancellation**: Comprehensive cancellation handling
- **Edge Case Handling**: No drivers available, connectivity issues

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- No external dependencies required

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd RideSharingService
```

2. Run the demo:

```bash
python3 run.py
```

### Sample Output

```
🚗 Ride Sharing System Demo - Design Patterns Showcase
============================================================

✅ Registered 2 riders and 4 drivers

📋 Demo 1: Basic Ride with Vehicle-Based Pricing
--------------------------------------------------
💰 Base fare: ₹717.11
Ride completed successfully

📋 Demo 2: Decorator Pattern - Pricing with Discount & Surge
--------------------------------------------------
💰 Final fare with decorators: ₹134.12
Ride completed successfully

... (additional demos)

💰 Driver Earnings & Ride History:
==================================================
🚗 John (Bajaj Auto)
   💵 Total Earnings: ₹149.42
   📋 Rides Completed: 3
```

## 🎭 Demo Scenarios

The demo includes 9 comprehensive scenarios:

### 1. **Basic Ride with Vehicle-Based Pricing**

- Demonstrates core ride functionality
- Shows vehicle-based fare calculation
- Driver matching and ride completion

### 2. **Decorator Pattern - Complex Pricing**

- 10% discount + 1.5x surge + 18% tax
- Shows composable pricing components
- Real-world pricing scenarios

### 3. **Different Vehicle Types**

- Luxury vehicle ride
- Higher fare calculation
- Premium service demonstration

### 4. **Observer Pattern - Notifications**

- Real-time driver notifications
- Ride status updates
- Automatic communication system

### 5. **State Pattern - Ride Transitions**

- Complete ride lifecycle
- State transition tracking
- Business rule enforcement

### 6. **Edge Case - No Available Drivers**

- System handles driver unavailability
- Graceful failure handling
- User experience considerations

### 7. **Ride Cancellation Scenario**

- Cancellation workflow
- State management during cancellation
- Business rule validation

### 8. **Driver Connectivity Issues**

- Driver goes offline during ride
- System resilience
- Real-world problem handling

### 9. **Multiple Riders - Same Driver**

- Driver capacity management
- Concurrent ride requests
- Resource allocation

## 📚 API Documentation

### Core System Methods

#### RideSharingSystem

```python
# Get singleton instance
system = RideSharingSystem.get_instance()

# Register users
rider = system.register_rider("Alice", "123-456-7890")
driver = system.register_driver("John", "111-222-3333", vehicle, location)

# Request ride
ride = system.request_ride(rider_id, pickup, destination, ride_type, pricing_decorator)

# Manage ride lifecycle
system.accept_ride(driver_id, ride)
system.start_ride(ride_id)
system.complete_ride(ride_id)
system.cancel_ride(ride_id, user)
```

#### Vehicle Factory

```python
# Create vehicles using factory pattern
auto_factory = AutoFactory()
sedan_factory = SedanFactory()
suv_factory = SUVFactory()
luxury_factory = LuxuryFactory()

vehicle = sedan_factory.create_vehicle("KA01-1234", "Toyota Camry")
```

#### Pricing Decorators

```python
# Create pricing with decorators
base_pricing = DistanceBasedPricingStrategy(base_fare=5.0, rate_per_km=8.0)
discount_pricing = DiscountDecorator(base_pricing, 0.1)  # 10% discount
surge_pricing = SurgeDecorator(discount_pricing, 1.5)   # 1.5x surge
final_pricing = TaxDecorator(surge_pricing, 0.18)       # 18% tax
```

## 💼 Business Logic

### Pricing Model

- **Base Fare**: Fixed amount per ride
- **Distance Rate**: Per kilometer pricing
- **Vehicle Multiplier**: Different rates for vehicle types
- **Surge Pricing**: Dynamic multiplier during high demand
- **Discounts**: Promotional pricing support
- **Taxes**: Automatic tax calculation

### Driver Earnings

- **Driver Commission**: 80% of ride fare
- **Platform Commission**: 20% of ride fare
- **Real-time Tracking**: Earnings updated after each ride
- **History Management**: Complete ride history tracking

### Ride States

1. **REQUESTED**: Initial ride request
2. **ACCEPTED**: Driver accepts the ride
3. **IN_PROGRESS**: Ride has started
4. **COMPLETED**: Ride finished successfully
5. **CANCELLED**: Ride cancelled by rider or driver

## 🚨 Edge Cases Handled

### Driver Unavailability

- No drivers available in area
- All drivers busy
- Drivers offline
- Graceful error messages

### Connectivity Issues

- Driver goes offline during ride
- Network connectivity problems
- Phone battery issues
- System resilience

### Business Logic Edge Cases

- Ride cancellation after acceptance
- Multiple riders requesting same driver
- Invalid ride states
- Payment failures

### Data Integrity

- Circular import prevention
- Type safety with TYPE_CHECKING
- Immutable objects where appropriate
- Thread-safe operations

## 🧪 Testing

The demo serves as a comprehensive test suite covering:

- All design patterns
- Edge cases and error scenarios
- Business logic validation
- System integration testing
- Performance under various conditions

## 🔧 Configuration

### Driver Matching Strategy

```python
# Configure maximum distance for driver matching
strategy = NearestDriverMatchingStrategy(max_distance=10.0)
system.set_driver_matching_strategy(strategy)
```

### Pricing Configuration

```python
# Configure base pricing
base_pricing = VehicleBasedPricingStrategy(base_fare=10.0)
```

## 📊 Performance Considerations

- **Singleton Pattern**: Reduces memory footprint
- **Factory Pattern**: Efficient object creation
- **Strategy Pattern**: Runtime algorithm switching
- **Observer Pattern**: Decoupled communication
- **State Pattern**: Efficient state management

## 🚀 Future Enhancements

- **Database Integration**: Persistent storage
- **Real-time Tracking**: GPS-based location updates
- **Payment Gateway**: External payment processing
- **Rating System**: Driver and rider ratings
- **Route Optimization**: Dynamic route calculation
- **Multi-language Support**: Internationalization
- **Microservices**: Service decomposition
- **Caching**: Redis integration
- **Monitoring**: System health monitoring
- **Analytics**: Business intelligence

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add comprehensive tests
5. Update documentation
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Amit** - _Initial work_ - [GitHub Profile]

## 🙏 Acknowledgments

- Design patterns inspiration from Gang of Four
- Real-world scenarios from Uber/Ola case studies
- Community feedback and suggestions

---

**Note**: This is a learning project demonstrating design patterns and system design principles. It's not intended for production use without additional security, scalability, and reliability enhancements.
