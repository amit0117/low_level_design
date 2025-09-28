# 🏗️ Splitwise Architecture - UML Class Diagram

## 📊 Visual Representation

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SPLITWISE ARCHITECTURE                            │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                SERVICE LAYER                                   │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐            │
│  │ SplitWiseService│    │   UserService   │    │  GroupService    │            │
│  │   (Singleton)   │◄───┤                 │    │                 │            │
│  │   (Facade)      │    │                 │    │                 │            │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘            │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                DOMAIN LAYER                                    │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐      │
│  │  User  │◄───┤  Group  │◄───┤ Expense │◄───┤Transaction│    │BalanceSheet│    │
│  │(Observer)│   │(Subject)│   │(Subject)│   │(Subject)│    │           │    │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘      │
│       │             │             │             │             │              │
│       └─────────────┼─────────────┼─────────────┼─────────────┘              │
│                     │             │             │                            │
│  ┌─────────┐        │             │             │                            │
│  │  Split  │◄───────┘             │             │                            │
│  └─────────┘                      │             │                            │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              STRATEGY LAYER                                   │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐            │
│  │ SplitStrategy   │◄───┤EqualSplitStrategy│    │PercentSplitStrategy│          │
│  │   (Abstract)    │    │                 │    │                 │            │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘            │
│         ▲                       │                       │                      │
│         │                       │                       │                      │
│         └───────────────────────┼───────────────────────┘                      │
│                                 │                                              │
│  ┌─────────────────┐            │                                              │
│  │ExactSplitStrategy│◄───────────┘                                              │
│  └─────────────────┘                                                          │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              BUILDER LAYER                                    │
│  ┌─────────────────┐                                                         │
│  │ ExpenseBuilder  │                                                         │
│  │   (Builder)     │                                                         │
│  └─────────────────┘                                                         │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              OBSERVER LAYER                                   │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐            │
│  │    Observer     │◄───┤   GroupSubject   │    │  ExpenseSubject  │            │
│  │   (Abstract)    │    │                 │    │                 │            │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘            │
│         ▲                       │                       │                      │
│         │                       │                       │                      │
│         └───────────────────────┼───────────────────────┘                      │
│                                 │                                              │
│  ┌─────────────────┐            │                                              │
│  │TransactionSubject│◄───────────┘                                              │
│  └─────────────────┘                                                          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🎯 Design Patterns Illustrated

### 1. **Singleton Pattern** 🔒

- `SplitWiseService` ensures single instance across the application
- Thread-safe implementation with double-checked locking

### 2. **Facade Pattern** 🏛️

- `SplitWiseService` provides simplified interface to complex subsystems
- Hides complexity of `UserService` and `GroupService`

### 3. **Strategy Pattern** ⚙️

- `SplitStrategy` abstract class with concrete implementations
- `EqualSplitStrategy`, `PercentSplitStrategy`, `ExactSplitStrategy`
- Runtime algorithm selection for expense splitting

### 4. **Observer Pattern** 👁️

- `User` implements `Observer` interface
- `Group`, `Expense`, `Transaction` extend `Subject` classes
- Real-time notifications for all events

### 5. **Builder Pattern** 🔨

- `ExpenseBuilder` constructs complex `Expense` objects
- Fluent interface with validation
- Handles optional parameters elegantly

## 🔗 Key Relationships

### **Composition Relationships**

- `User` **owns** `BalanceSheet` (1:1)
- `Group` **contains** `Expense` (1:many)
- `Expense` **contains** `Split` (1:many)
- `User` **member of** `Group` (many:many)

### **Dependency Relationships**

- `Expense` **uses** `SplitStrategy` (dependency injection)
- `ExpenseBuilder` **builds** `Expense` (factory method)
- `Transaction` **involves** `User` (bidirectional)

### **Inheritance Relationships**

- `User` **implements** `Observer`
- `Group` **extends** `GroupSubject`
- `Expense` **extends** `ExpenseSubject`
- `Transaction` **extends** `TransactionSubject`
- All split strategies **implement** `SplitStrategy`

## 🚀 Advanced Features

### **Thread Safety** 🔒

- `BalanceSheet` uses `Lock` for concurrent access
- `SplitWiseService` uses double-checked locking
- Thread-safe balance adjustments

### **Debt Simplification** 🧮

- `Group.simplify_expenses()` uses heap-based algorithm
- Minimizes number of transactions
- Optimal creditor-debtor pairing

### **Real-time Notifications** 📢

- Observer pattern for instant updates
- Method-specific notifications (`expense_update`, `transaction_update`, `update_group`)
- Event-driven architecture

## 📊 Data Flow

```
User Request → SplitWiseService → UserService/GroupService → Domain Models → Observer Notifications
     ↓              ↓                    ↓                    ↓                    ↓
  Response ←   Facade Layer ←    Service Layer ←    Domain Layer ←    Notification Layer
```

## 🎨 Architecture Benefits

1. **Separation of Concerns**: Each layer has distinct responsibilities
2. **Loose Coupling**: Dependencies flow inward (Dependency Inversion)
3. **High Cohesion**: Related functionality grouped together
4. **Extensibility**: Easy to add new split strategies or observers
5. **Testability**: Each component can be tested in isolation
6. **Maintainability**: Clear structure makes code easy to understand and modify
