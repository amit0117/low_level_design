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

## 📊 Entity Relationship Diagram

### Core Entities and Relationships

```
┌─────────────────────────────────────┐
│   RestrauntManagementApp            │
│─────────────────────────────────────│
│ (Singleton/Facade)                  │
│ - table_service                     │
│ - order_service                     │
│ - inventory_service                 │
│ - staff_repo                        │
│ - menu_repo                         │
└──────┬──────────────────────────────┘
       │
       │ 1..* (manages)
       │
       ▼
┌─────────────────────────────────────┐
│            Table                    │
│─────────────────────────────────────│
│ table_number                        │
│ capacity                            │
│ status (TableStatus)                │
│ state (TableState)                  │
│ observers (List<Observer>)          │
└──────┬──────────────────────────────┘
       │
       │ 1..* (has)
       │
       ▼
┌─────────────────────────────────────┐
│            Order                    │
│─────────────────────────────────────│
│ order_id                            │
│ table (Table)                       │
│ customer (Customer)                 │
│ items (List<OrderItem>)             │
│ total_amount                        │
│ status (OrderStatus)                │
│ observers (List<Observer>)          │
└──────┬──────────────────────────────┘
       │
       │ 1..* (contains)
       │
       ▼
┌─────────────────────────────────────┐
│          OrderItem                  │
│─────────────────────────────────────│
│ id                                  │
│ item (Item)                         │
│ quantity                            │
│ status (OrderItemStatus)            │
│ state (OrderItemState)              │
│ subtotal                            │
└──────┬──────────────────────────────┘
       │
       │ references
       │
       ▼
┌─────────────────────────────────────┐
│            Item                     │
│─────────────────────────────────────│
│ id                                  │
│ name                                │
│ price                               │
│ type (ItemType)                     │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┐
       ▼              ▼
┌─────────────┐ ┌─────────────┐
│  VegItem    │ │ NonVegItem  │
└─────────────┘ └─────────────┘

┌─────────────────────────────────────┐
│          Customer                   │
│─────────────────────────────────────│
│ id                                  │
│ name                                │
│ (Observer for Order updates)        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│            Staff                    │
│─────────────────────────────────────│
│ id                                  │
│ name                                │
│ role (StaffRole)                    │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Manager   │ │    Chef     │ │   Waiter    │
└─────────────┘ └─────────────┘ └─────────────┘

┌─────────────────────────────────────┐
│          Payment                    │
│─────────────────────────────────────│
│ amount                              │
│ payment_method (PaymentMethod)      │
│ payment_status (PaymentStatus)      │
│ payment_strategy (PaymentStrategy)  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│         Inventory                   │
│─────────────────────────────────────│
│ item (Item)                         │
│ quantity                            │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│            Menu                     │
│─────────────────────────────────────│
│ items (List<Item>)                  │
└─────────────────────────────────────┘
```

### Entity Relationships

1. **RestrauntManagementApp ↔ Table** (One-to-Many via Repository)

   - App manages multiple Tables
   - Tables stored in TableRepository

2. **RestrauntManagementApp ↔ Order** (One-to-Many via Repository)

   - App manages multiple Orders
   - Orders stored in OrderRepository

3. **Table ↔ Order** (One-to-Many)

   - A Table can have multiple Orders (over time)
   - Each Order is associated with one Table
   - Only one active Order per table at a time

4. **Order ↔ OrderItem** (One-to-Many)

   - An Order contains multiple OrderItems
   - Each OrderItem belongs to one Order

5. **OrderItem ↔ Item** (Many-to-One)

   - An OrderItem references one Item
   - An Item can be referenced by multiple OrderItems

6. **Item Inheritance Hierarchy**

   - `Item` (base class)
   - `VegItem`, `NonVegItem` (subclasses)

7. **Order ↔ Customer** (Many-to-One)

   - An Order is placed by one Customer
   - A Customer can place multiple Orders

8. **Table ↔ TableState** (One-to-One)

   - Each Table has one current State
   - State transitions: Available → Reserved → Occupied → Available

9. **OrderItem ↔ OrderItemState** (One-to-One)

   - Each OrderItem has one current State
   - State transitions: Ordered → Preparing → Ready → Served

10. **Order ↔ Payment** (One-to-One)

    - An Order can have one Payment
    - Payment created when order is paid

11. **Item ↔ Inventory** (One-to-One)

    - An Item has one Inventory record
    - Inventory tracks stock quantity

12. **Menu ↔ Item** (One-to-Many)

    - A Menu contains multiple Items
    - Items can be added/removed from Menu

13. **Staff Inheritance Hierarchy**

    - `Staff` (base class)
    - `Manager`, `Chef`, `Waiter` (subclasses)

14. **Observer Pattern Relationships**

    - Order implements `OrderSubject` - notifies on status changes
    - Table implements `TableSubject` - notifies on state changes
    - Customer implements `OrderObserver` - receives order notifications

15. **Strategy Pattern Relationships**

    - Payment uses `PaymentStrategy` (delegates payment processing)
    - Supports CreditCardPayment, UPIPayment, CashPayment

16. **Decorator Pattern Relationships**
    - Bill generation uses decorators: TaxDecorator, ServiceChargeDecorator, DiscountDecorator
    - Decorators wrap base bill calculation

## 🔄 Data Flow Diagrams

### 1. Order Creation Flow

```
┌──────────┐
│ Customer │
└────┬─────┘
     │
     │ 1. create_order_with_items()
     ▼
┌─────────────────┐
│RestrauntMgmtApp │
└────┬────────────┘
     │
     │ 2. order_service.create_order()
     ▼
┌─────────────────┐
│  OrderService   │
└────┬────────────┘
     │
     │ 3. Validate table
     │ 4. Check inventory
     │ 5. Create Order & OrderItems
     ▼
┌─────────────────┐
│     Order       │
│  - OrderItems   │
└────┬────────────┘
     │
     │ 6. Update inventory
     │ 7. notify_observers()
     ▼
┌─────────────────┐
│   Customer      │
│  (Notified)     │
└─────────────────┘
```

### 2. Order Processing Flow

```
┌──────────┐
│   Staff  │
└────┬─────┘
     │
     │ 1. process_order(order_id)
     ▼
┌─────────────────┐
│RestrauntMgmtApp │
└────┬────────────┘
     │
     │ 2. order_service.process_order()
     ▼
┌─────────────────┐
│  OrderService   │
└────┬────────────┘
     │
     │ 3. Create Command
     ▼
┌─────────────────┐
│ PrepareOrder    │
│    Command      │
└────┬────────────┘
     │
     │ 4. execute()
     │ 5. Update OrderItem states
     ▼
┌─────────────────┐
│  OrderItems     │
│  (Preparing)    │
└────┬────────────┘
     │
     │ 6. notify_observers()
     ▼
┌─────────────────┐
│   Observers     │
│  (Notified)     │
└─────────────────┘
```

### 3. Payment Processing Flow

```
┌──────────┐
│ Customer │
└────┬─────┘
     │
     │ 1. process_payment(order_id, strategy)
     ▼
┌─────────────────┐
│RestrauntMgmtApp │
└────┬────────────┘
     │
     │ 2. Calculate bill
     │ 3. Apply decorators
     ▼
┌─────────────────┐
│ Bill Decorators │
│ - Tax           │
│ - ServiceCharge │
│ - Discount      │
└────┬────────────┘
     │
     │ 4. Process payment
     ▼
┌─────────────────┐
│ PaymentStrategy │
│  (Strategy)     │
└────┬────────────┘
     │
     │ 5. Execute payment
     ▼
┌─────────────────┐
│  PaymentResult  │
└─────────────────┘
```

### 4. Table Reservation Flow

```
┌──────────┐
│ Customer │
└────┬─────┘
     │
     │ 1. reserve_table(table_num, customer, size)
     ▼
┌─────────────────┐
│RestrauntMgmtApp │
└────┬────────────┘
     │
     │ 2. table_service.reserve_table()
     ▼
┌─────────────────┐
│  TableService   │
└────┬────────────┘
     │
     │ 3. Get table
     │ 4. Check availability
     │ 5. Change state
     ▼
┌─────────────────┐
│     Table       │
│  (Reserved)     │
└────┬────────────┘
     │
     │ 6. notify_observers()
     ▼
┌─────────────────┐
│   Observers     │
│  (Notified)     │
└─────────────────┘
```

## 📋 Entity Attributes Summary

### Table Entity

- `table_number`: Unique table identifier
- `capacity`: Maximum number of people
- `status`: TableStatus (AVAILABLE, RESERVED, OCCUPIED)
- `state`: TableState object
- `observers`: List of Observer objects

### Order Entity

- `order_id`: Unique order identifier
- `table`: Reference to Table
- `customer`: Reference to Customer
- `items`: List of OrderItem objects
- `total_amount`: Total order amount
- `status`: OrderStatus
- `observers`: List of Observer objects

### OrderItem Entity

- `id`: Unique identifier
- `item`: Reference to Item
- `quantity`: Quantity ordered
- `status`: OrderItemStatus
- `state`: OrderItemState object
- `subtotal`: Item price × quantity

### Item Entity

- `id`: Unique identifier
- `name`: Item name
- `price`: Item price
- `type`: ItemType (VEG, NON_VEG)

### Customer Entity

- `id`: Unique identifier
- `name`: Customer name
- Implements OrderObserver interface

### Staff Entity

- `id`: Unique identifier
- `name`: Staff name
- `role`: StaffRole (MANAGER, CHEF, WAITER)

### Payment Entity

- `amount`: Payment amount
- `payment_method`: PaymentMethod (CASH, CREDIT_CARD, UPI)
- `payment_status`: PaymentStatus (PENDING, COMPLETED, FAILED)
- `payment_strategy`: PaymentStrategy object

### Inventory Entity

- `item`: Reference to Item
- `quantity`: Available stock quantity

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
