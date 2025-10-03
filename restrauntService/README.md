# Restaurant Management System

A comprehensive restaurant management system built using Python and implementing various design patterns to demonstrate object-oriented programming principles and software architecture best practices.

## 🏗️ Architecture Overview

The system follows a modular architecture with clear separation of concerns:

```
restrauntService/
├── restraunt_management_app.py    # Main facade class (Singleton)
├── run.py                         # Demo application
└── app/
    ├── models/                    # Domain entities
    ├── commands/                  # Command pattern implementation
    ├── decorators/                # Decorator pattern for billing
    ├── observers/                 # Observer pattern implementation
    ├── states/                    # State pattern implementation
    ├── strategies/                # Strategy pattern for payments
    └── exceptions/                # Custom exception classes
```

## 🎯 Design Patterns Implemented

### 1. **Singleton Pattern**

- **Class**: `RestrauntManagementApp`
- **Purpose**: Ensures only one instance of the restaurant management system exists
- **Implementation**: Thread-safe singleton with double-checked locking

### 2. **Facade Pattern**

- **Class**: `RestrauntManagementApp`
- **Purpose**: Provides a simplified interface to complex subsystem operations
- **Benefits**: Hides complexity of table management, order processing, inventory, etc.

### 3. **Observer Pattern**

- **Classes**: `OrderObserver`, `TableObserver`, `InventoryObserver`
- **Purpose**: Notifies stakeholders about order status changes, table state changes, and inventory updates
- **Implementation**: Subject-Observer relationship with thread-safe notifications

### 4. **State Pattern**

- **Classes**: `TableState`, `OrderItemState`
- **Purpose**: Manages table states (Available/Reserved/Occupied) and order item states (Ordered/Preparing/Ready/Served)
- **Benefits**: Encapsulates state-specific behavior and transitions

### 5. **Command Pattern**

- **Classes**: `PrepareOrderCommand`, `ServeOrderCommand`
- **Purpose**: Encapsulates requests as objects, allowing for queuing, logging, and undo operations
- **Benefits**: Decouples the object that invokes the operation from the one that performs it

### 6. **Decorator Pattern**

- **Classes**: `TaxDecorator`, `ServiceChargeDecorator`, `DiscountDecorator`
- **Purpose**: Dynamically adds responsibilities to bill items (tax, service charge, discounts)
- **Benefits**: Flexible bill composition without modifying base classes

### 7. **Strategy Pattern**

- **Classes**: `CreditCardPayment`, `UPIPayment`, `CashPayment`
- **Purpose**: Encapsulates different payment algorithms and makes them interchangeable
- **Benefits**: Easy to add new payment methods without modifying existing code

## 🚀 Key Features

### Table Management

- **Reservation System**: Reserve tables for customers
- **State Management**: Track table availability (Available → Reserved → Occupied → Available)
- **Capacity Validation**: Ensure group size doesn't exceed table capacity

### Order Processing

- **Order Creation**: Create orders with multiple items
- **Inventory Validation**: Check stock availability before processing
- **Kitchen Workflow**: Chef preparation → Ready for pickup → Waiter serving
- **State Tracking**: Monitor order item states throughout the process

### Inventory Management

- **Stock Tracking**: Monitor item quantities in real-time
- **Automatic Deduction**: Reduce inventory when orders are processed
- **Restocking**: Add items back to inventory
- **Low Stock Notifications**: Alert managers when items run out

### Billing System

- **Dynamic Pricing**: Apply taxes, service charges, and discounts
- **Itemized Bills**: Detailed breakdown of ordered items
- **Multiple Payment Methods**: Support for Credit Card, UPI, and Cash payments

### Staff Management

- **Role-based Access**: Different staff roles (Manager, Chef, Waiter)
- **Task Assignment**: Automatic assignment of orders to available staff
- **Notification System**: Staff receive updates about their assigned tasks

## 📋 Usage Examples

### Basic Restaurant Setup

```python
from restraunt_management_app import RestrauntManagementApp
from app.models.staff import Manager, Chef, Waiter
from app.models.table import Table
from app.models.item import VegItem, NonVegItem

# Get singleton instance
rms = RestrauntManagementApp.get_instance()

# Add staff
manager = Manager("John Manager")
chef = Chef("Gordon Chef")
waiter = Waiter("Alice Waiter")

rms.add_manager(manager)
rms.add_chef(chef)
rms.add_waiter(waiter)

# Add tables
table = Table(1, 4)  # Table 1 with capacity 4
rms.add_table(table)

# Add menu items
pizza = VegItem("Margherita Pizza", 299.0)
rms.add_item_to_menu(pizza)
rms.add_item_to_inventory(pizza, 20)
```

### Order Processing Workflow

```python
from app.models.order_item import OrderItem

# Reserve and occupy table
rms.reserve_table(1, "Alice Customer", 2)
rms.occupy_table(1)

# Create order
order_items = [OrderItem("", pizza, 1)]
order = rms.create_order_with_items(1, "Alice Customer", order_items)

# Process order
rms.process_order(order.get_order_id())
rms.mark_order_items_ready(order.get_order_id())
rms.serve_order(order.get_order_id())

# Generate bill and process payment
rms.generate_bill(order.get_order_id(), tax_rate=0.18, service_charge=50.0)
from app.strategies.payment_strategy import UPIPayment
payment_result = rms.process_payment(UPIPayment(), 400.0)

# Release table
rms.release_table(1)
```

## 🛠️ Running the Demo

```bash
cd low_level_design/restrauntService
python3 run.py
```

The demo showcases:

- Complete restaurant workflow from table reservation to payment
- Multiple customer scenarios with different payment methods
- Edge case handling (out-of-stock, validation errors, payment failures)
- All design patterns in action

## 🔧 Error Handling

The system includes comprehensive error handling for:

- **Inventory Management**: `InsufficientStockException` when ordering more than available
- **Menu Validation**: `MissingItemException` when ordering non-existent items
- **Table Management**: Validation for table states and capacity
- **Payment Processing**: Handling of failed payment scenarios
- **Order Processing**: Validation of order states and staff availability

## 🧪 Testing Scenarios

The demo includes test cases for:

1. **Happy Path**: Normal restaurant operations
2. **Out-of-Stock**: Ordering more items than available
3. **Table Validation**: Ordering from unoccupied tables
4. **Payment Failure**: Handling failed payment attempts
5. **Capacity Limits**: Group size exceeding table capacity

## 📊 System Status

The system provides real-time status information:

- Available/occupied/reserved tables
- Active orders and their states
- Inventory levels
- Staff availability

## 🔒 Thread Safety

The system is designed for concurrent access with:

- Thread-safe singleton implementation
- Locked operations for critical sections
- Thread-safe observer notifications
- Concurrent order processing support

## 🎓 Learning Objectives

This project demonstrates:

- **Object-Oriented Design**: Proper use of inheritance, polymorphism, and encapsulation
- **Design Patterns**: Real-world implementation of 7 common design patterns
- **Software Architecture**: Modular design with clear separation of concerns
- **Error Handling**: Comprehensive exception handling and validation
- **Concurrent Programming**: Thread-safe operations and synchronization
- **Business Logic**: Real-world restaurant management scenarios

## 📝 Future Enhancements

Potential improvements:

- Database integration for persistent storage
- REST API for external system integration
- Real-time notifications via WebSocket
- Advanced reporting and analytics
- Multi-location restaurant support
- Customer loyalty program integration

---

**Note**: This is a demonstration project showcasing design patterns and software architecture principles. It's not intended for production use without additional security, validation, and error handling considerations.
