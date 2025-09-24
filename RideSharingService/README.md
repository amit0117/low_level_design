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
