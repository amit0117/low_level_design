# 🍽️ Restaurant Management System

A comprehensive restaurant management system implementing multiple design patterns and SOLID principles.

## 🏗️ Architecture Overview

This system follows a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    FACADE LAYER                             │
│              RestrauntManagementApp                          │
│         (Simplified interface for all operations)          │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                   SERVICE LAYER                              │
│  TableService  │  OrderService  │  InventoryService         │
│  (Business Logic - Only where needed)                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                 REPOSITORY LAYER                             │
│ TableRepo │ OrderRepo │ StaffRepo │ MenuRepo │ InventoryRepo│
│         (Data Access - Singleton Pattern)                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                   DOMAIN LAYER                               │
│   Models, States, Strategies, Decorators, Observers          │
│              (Business Entities & Behaviors)                 │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Key Architectural Decisions

### ✅ **Services Only Where Business Logic Exists**

- **TableService**: Complex table state management and availability logic
- **OrderService**: Order processing, validation, and workflow orchestration
- **InventoryService**: Stock management and validation logic

### ✅ **Direct Repository Access for Simple Operations**

- Staff management: Direct `StaffRepository` access
- Menu management: Direct `MenuRepository` access
- No unnecessary service layer for CRUD operations

### ✅ **Singleton Repositories**

- Ensures data consistency across services
- Thread-safe implementation
- Single source of truth for data

## 📁 Project Structure

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

## 🎨 Design Patterns Implemented

1. **Singleton Pattern** - Repositories ensure single data source
2. **Facade Pattern** - `RestrauntManagementApp` provides simplified interface
3. **Repository Pattern** - Data access abstraction
4. **Service Pattern** - Business logic encapsulation (where needed)
5. **Observer Pattern** - Order, table, and inventory notifications
6. **State Pattern** - Table and order item state management
7. **Command Pattern** - Order preparation and serving commands
8. **Decorator Pattern** - Bill generation with tax, service charge, discounts
9. **Strategy Pattern** - Payment processing strategies

## 🚀 Usage Examples

### Simple Operations (Direct Repository Access)

```python
# Staff Management
rms.add_chef(chef)
chefs = rms.get_chefs()

# Menu Management
rms.add_item_to_menu(item)
menu_items = rms.get_menu().find_all_items()
```

### Complex Operations (Service Layer)

```python
# Table Management (Complex state logic)
rms.add_table(table)
rms.reserve_table(1, "Customer")
rms.occupy_table(1)

# Order Processing (Complex workflow)
order = rms.create_order_with_items(1, "Customer", items)
rms.process_order(order.get_order_id())
rms.serve_order(order.get_order_id())

# Inventory Management (Complex validation)
rms.add_item_to_inventory(item, quantity)
rms.remove_item_from_inventory(item, quantity)
```

## 🎯 SOLID Principles Applied

- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Extensible through strategies and decorators
- **Liskov Substitution**: All implementations are interchangeable
- **Interface Segregation**: Focused interfaces for specific needs
- **Dependency Inversion**: Depends on abstractions, not concretions

## 🏃‍♂️ Running the Demo

```bash
cd restrauntService
python3 run.py
```

The demo showcases:

- Complete customer journey (arrival → order → payment → departure)
- Multiple payment methods (UPI, Credit Card, Cash)
- Edge cases (insufficient inventory, table conflicts)
- Real-time status updates and notifications

## ✨ Key Features

- **Thread-safe operations** with proper locking
- **Comprehensive error handling** with custom exceptions
- **Real-time notifications** via Observer pattern
- **Flexible payment processing** with Strategy pattern
- **Dynamic bill generation** with Decorator pattern
- **State management** for tables and order items
- **Command-based operations** for order processing

## 🎉 Simplified Architecture Benefits

- **No unnecessary service layers** - Services only where business logic exists
- **Direct repository access** for simple CRUD operations
- **Cleaner code** with less indirection
- **Better performance** with fewer method calls
- **Easier maintenance** with simpler structure
- **Clear separation** between complex and simple operations
