# Restaurant Management System

A comprehensive restaurant management system built using Python and implementing various design patterns to demonstrate object-oriented programming principles and software architecture best practices. The system follows **SOLID principles** and implements a clean **Repository-Service-Facade architecture**.

## 🏗️ Architecture Overview

The system follows a **layered architecture** with clear separation of concerns following SOLID principles:

```
┌─────────────────────────────────────┐
│           FACADE LAYER              │
│     RestrauntManagementApp          │
└─────────────────────────────────────┘
                    │
┌─────────────────────────────────────┐
│          SERVICE LAYER               │
│  TableService │ OrderService │ etc.  │
└─────────────────────────────────────┘
                    │
┌─────────────────────────────────────┐
│        REPOSITORY LAYER              │
│ TableRepo │ OrderRepo │ StaffRepo    │
└─────────────────────────────────────┘
                    │
┌─────────────────────────────────────┐
│          DATA LAYER                  │
│     Models & Business Objects        │
└─────────────────────────────────────┘
```

### 📁 Detailed Project Structure

```
restrauntService/
├── restraunt_management_app.py    # Main Facade class (Singleton)
├── run.py                         # Demo application showcasing all features
├── README.md                      # This documentation file
└── app/
    ├── models/                    # Domain entities and business objects
    │   ├── customer.py            # Customer model with Observer pattern
    │   ├── enums.py               # Enums for OrderItemStatus, StaffRole, etc.
    │   ├── inventory.py           # Inventory management
    │   ├── item.py                # Menu items (VegItem, NonVegItem)
    │   ├── menu.py                # Menu management
    │   ├── order.py               # Order entity
    │   ├── order_item.py          # OrderItem with State pattern
    │   ├── payment.py             # Payment model
    │   ├── staff.py               # Staff hierarchy (Manager, Chef, Waiter)
    │   └── table.py               # Table with State pattern
    │
    ├── repositories/              # Data Access Layer (Singleton Pattern)
    │   ├── table_repository.py    # Table data operations
    │   ├── order_repository.py    # Order data operations
    │   ├── staff_repository.py    # Staff data operations
    │   ├── menu_repository.py     # Menu data operations
    │   └── inventory_repository.py # Inventory data operations
    │
    ├── services/                  # Business Logic Layer
    │   ├── table_service.py       # Table business logic
    │   ├── order_service.py       # Order business logic
    │   ├── staff_service.py       # Staff business logic
    │   ├── menu_service.py        # Menu business logic
    │   └── inventory_service.py  # Inventory business logic
    │
    ├── commands/                  # Command Pattern implementation
    │   └── order_command.py       # PrepareOrderCommand, ServeOrderCommand
    │
    ├── decorators/                # Decorator Pattern for billing
    │   └── bill_decorator.py      # TaxDecorator, ServiceChargeDecorator, DiscountDecorator
    │
    ├── observers/                 # Observer Pattern implementation
    │   ├── order_observer.py      # Order status notifications
    │   ├── table_observer.py      # Table state notifications
    │   └── inventory_observer.py  # Inventory change notifications
    │
    ├── states/                    # State Pattern implementation
    │   ├── table_state.py         # Table states (Available, Reserved, Occupied)
    │   └── order_item_state.py    # OrderItem states (Ordered, Preparing, Ready, Served)
    │
    ├── strategies/                # Strategy Pattern for payments
    │   └── payment_strategy.py    # CreditCardPayment, UPIPayment, CashPayment
    │
    └── exceptions/                # Custom exception classes
        ├── inventory.py           # InsufficientStockException
        └── item.py                # MissingItemException
```

### 🏗️ Architecture Layers Explained

#### **1. Facade Layer** (`restraunt_management_app.py`)

- **Purpose**: Provides simplified interface to complex subsystem
- **Responsibilities**:
  - Orchestrates service calls
  - Handles complex workflows
  - Provides high-level operations
- **Pattern**: Singleton + Facade

#### **2. Service Layer** (`app/services/`)

- **Purpose**: Encapsulates business logic and orchestrates repositories
- **Responsibilities**:
  - Business rule validation
  - Transaction management
  - Cross-domain operations
- **Pattern**: Service Pattern

#### **3. Repository Layer** (`app/repositories/`)

- **Purpose**: Abstracts data access and provides uniform interface
- **Responsibilities**:
  - Data persistence operations
  - Query abstraction
  - Database independence
- **Pattern**: Repository + Singleton

#### **4. Domain Layer** (`app/models/`)

- **Purpose**: Contains business entities and domain logic
- **Responsibilities**:
  - Business object representation
  - Domain-specific behavior
  - State management
- **Patterns**: State, Observer, Inheritance

#### **5. Cross-Cutting Concerns**

- **Commands** (`app/commands/`): Request encapsulation
- **Decorators** (`app/decorators/`): Dynamic behavior extension
- **Observers** (`app/observers/`): Event notifications
- **States** (`app/states/`): Object state management
- **Strategies** (`app/strategies/`): Algorithm interchangeability
- **Exceptions** (`app/exceptions/`): Error handling

## 🎯 SOLID Principles Implementation

### 1. **Single Responsibility Principle (SRP)**

- Each repository handles only one type of data access
- Each service handles only one domain's business logic
- Each class has a single, well-defined responsibility

### 2. **Open/Closed Principle (OCP)**

- Services are open for extension but closed for modification
- New payment strategies can be added without changing existing code
- New decorators can be added without modifying base classes

### 3. **Liskov Substitution Principle (LSP)**

- All repositories implement consistent interfaces
- Payment strategies are interchangeable
- Observer implementations can be substituted

### 4. **Interface Segregation Principle (ISP)**

- Focused, cohesive interfaces for each repository/service
- No client is forced to depend on methods it doesn't use

### 5. **Dependency Inversion Principle (DIP)**

- Services depend on repository abstractions, not concrete implementations
- High-level modules don't depend on low-level modules

## 🎨 Design Patterns Implemented

### 1. **Repository Pattern**

- **Classes**: `TableRepository`, `OrderRepository`, `StaffRepository`, `MenuRepository`, `InventoryRepository`
- **Purpose**: Abstracts data access logic and provides a uniform interface
- **Benefits**: Clean separation of data access, easier testing, database independence

### 2. **Service Pattern**

- **Classes**: `TableService`, `OrderService`, `InventoryService`, `StaffService`
- **Purpose**: Encapsulates business logic and orchestrates repositories
- **Benefits**: Business logic centralization, transaction management, validation

### 3. **Facade Pattern**

- **Class**: `RestrauntManagementApp`
- **Purpose**: Provides a simplified interface to complex subsystem operations
- **Benefits**: Hides complexity, provides high-level operations, easier client usage

### 4. **Singleton Pattern**

- **Class**: `RestrauntManagementApp`
- **Purpose**: Ensures only one instance of the restaurant management system exists
- **Implementation**: Thread-safe singleton with double-checked locking

### 5. **Observer Pattern**

- **Classes**: `OrderObserver`, `TableObserver`, `InventoryObserver`
- **Purpose**: Notifies stakeholders about system state changes
- **Implementation**: Subject-Observer relationship with thread-safe notifications

### 6. **State Pattern**

- **Classes**: `TableState`, `OrderItemState`
- **Purpose**: Manages object states and transitions
- **Benefits**: Encapsulates state-specific behavior, clear state transitions

### 7. **Command Pattern**

- **Classes**: `PrepareOrderCommand`, `ServeOrderCommand`
- **Purpose**: Encapsulates requests as objects
- **Benefits**: Decoupling, queuing, logging, undo operations

### 8. **Decorator Pattern**

- **Classes**: `TaxDecorator`, `ServiceChargeDecorator`, `DiscountDecorator`
- **Purpose**: Dynamically adds responsibilities to objects
- **Benefits**: Flexible composition, runtime behavior modification

### 9. **Strategy Pattern**

- **Classes**: `CreditCardPayment`, `UPIPayment`, `CashPayment`
- **Purpose**: Encapsulates algorithms and makes them interchangeable
- **Benefits**: Easy algorithm switching, open/closed principle compliance

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

# Get singleton instance (Facade)
rms = RestrauntManagementApp.get_instance()

# Add staff (delegates to StaffService)
manager = Manager("John Manager")
chef = Chef("Gordon Chef")
waiter = Waiter("Alice Waiter")

rms.add_manager(manager)  # → StaffService.add_staff_member() → StaffRepository.save_manager()
rms.add_chef(chef)       # → StaffService.add_staff_member() → StaffRepository.save_chef()
rms.add_waiter(waiter)   # → StaffService.add_staff_member() → StaffRepository.save_waiter()

# Add tables (delegates to TableService)
table = Table(1, 4)  # Table 1 with capacity 4
rms.add_table(table)  # → TableService.add_table() → TableRepository.save()

# Add menu items (delegates to MenuService/InventoryService)
pizza = VegItem("Margherita Pizza", 299.0)
rms.add_item_to_menu(pizza)        # → MenuService.add_item_to_menu() → MenuRepository.save_item()
rms.add_item_to_inventory(pizza, 20)  # → InventoryService.add_item_to_inventory()
```

### Order Processing Workflow

```python
from app.models.order_item import OrderItem

# Table management (delegates to TableService)
rms.reserve_table(1, "Alice Customer", 2)  # → TableService.reserve_table()
rms.occupy_table(1)                        # → TableService.occupy_table()

# Order creation (delegates to OrderService)
order_items = [OrderItem("", pizza, 1)]
order = rms.create_order_with_items(1, "Alice Customer", order_items)
# → OrderService.create_order() → validates table, menu, inventory

# Order processing (delegates to OrderService)
rms.process_order(order.get_order_id())        # → OrderService.process_order()
rms.mark_order_items_ready(order.get_order_id())  # → OrderService.mark_order_items_ready()
rms.serve_order(order.get_order_id())          # → OrderService.serve_order()

# Billing and payment (Facade handles directly)
rms.generate_bill(order.get_order_id(), tax_rate=0.18, service_charge=50.0)
from app.strategies.payment_strategy import UPIPayment
payment_result = rms.process_payment(UPIPayment(), 400.0)

# Table release (delegates to TableService)
rms.release_table(1)  # → TableService.release_table()
```

### Advanced Workflow (Complete Dining Experience)

```python
# Single method call orchestrates entire workflow
order = rms.complete_dining_experience(
    table_number=1,
    customer_name="Alice Customer",
    item_orders=[OrderItem("", pizza, 1)],
    chef_name="Gordon Chef",
    waiter_name="Alice Waiter"
)
# This method orchestrates:
# 1. TableService.reserve_table()
# 2. TableService.occupy_table()
# 3. OrderService.create_order()
# 4. OrderService.process_order()
# 5. OrderService.mark_order_items_ready()
# 6. OrderService.serve_order()
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

## 🎨 Simplified Architecture Features

### **Clean Service Constructors**

- **Simplified**: Services use clean constructors without complex dependency injection
- **Singleton Repositories**: All repositories are singletons, ensuring shared state
- **Auto-initialization**: Services automatically get repository instances
- **No Boilerplate**: Removed verbose docstrings and complex parameter passing

### **Streamlined Code Structure**

- **Self-Documenting**: Method names clearly indicate functionality
- **Concise**: Removed verbose documentation for cleaner code
- **Maintainable**: Easier to read and modify
- **Professional**: Follows modern Python coding standards

## 🏆 Architecture Benefits

### **Maintainability**

- Each file has a single, clear responsibility
- Changes to one layer don't affect others
- Easy to locate and fix bugs

### **Testability**

- Individual components can be unit tested in isolation
- Mock repositories for service testing
- Clear interfaces for dependency injection

### **Scalability**

- Easy to add new repositories/services without affecting existing code
- Horizontal scaling of services
- Database independence through repository abstraction

### **Reusability**

- Services can be reused across different facades
- Repository patterns can be applied to other domains
- Business logic is centralized and reusable

### **Flexibility**

- Easy to swap implementations (e.g., different databases)
- New features can be added without modifying existing code
- Payment strategies, decorators, and observers are easily extensible

## 🎓 Learning Objectives

This project demonstrates:

- **SOLID Principles**: Complete implementation of all 5 SOLID principles
- **Clean Architecture**: Repository-Service-Facade layered architecture
- **Design Patterns**: Real-world implementation of 9 design patterns
- **Object-Oriented Design**: Proper use of inheritance, polymorphism, and encapsulation
- **Separation of Concerns**: Clear boundaries between data access, business logic, and presentation
- **Dependency Injection**: Services depend on abstractions, not concrete implementations
- **Error Handling**: Comprehensive exception handling and validation
- **Concurrent Programming**: Thread-safe operations and synchronization
- **Business Logic**: Real-world restaurant management scenarios
- **Code Organization**: Single Responsibility Principle in file structure

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
