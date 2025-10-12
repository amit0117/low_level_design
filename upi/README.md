# UPI Payment System

A comprehensive UPI (Unified Payments Interface) payment system implementation demonstrating various design patterns and architectural principles. This project showcases a complete end-to-end payment processing system with cross-bank transfers, fraud detection, rate limiting, real-time notifications, and multiple payment methods.

## 🚀 Features

### Core Functionality

- **User Management** - Complete user registration and account management
- **Cross-Bank Transfers** - Seamless money transfers between different banks (HDFC, SBI)
- **Multiple Payment Methods** - UPI Push/Pull, Credit Card, Debit Card, Net Banking, Wallet
- **Fraud Detection** - Advanced fraud detection with velocity checks and suspicious transaction monitoring
- **Rate Limiting** - Per-user rate limiting to prevent abuse
- **Real-time Notifications** - Observer pattern for payment and transaction updates
- **Transaction Management** - Complete transaction lifecycle with state management
- **Bank Integration** - Abstract factory pattern for different bank integrations
- **Security** - Proxy pattern for access control and authentication
- **Error Handling** - Comprehensive exception handling and validation

### Design Patterns Implemented

- **Facade Pattern** - UPIApp provides simplified interface to complex system
- **Abstract Factory Pattern** - Bank-specific component creation (HDFC, SBI)
- **Adapter Pattern** - Standardized bank API communication
- **Chain of Responsibility** - Sequential payment processing (Validation → Authentication → Fraud → Routing → Settlement)
- **Command Pattern** - Payment operations with undo/redo capabilities
- **Decorator Pattern** - Fraud detection enhancement without modifying core logic
- **Observer Pattern** - Real-time notifications for payments, transactions, and account changes
- **Proxy Pattern** - Access control, rate limiting, and security layers
- **Strategy Pattern** - Different payment method implementations
- **State Pattern** - Transaction lifecycle management
- **Repository Pattern** - Clean data access layer
- **Service Pattern** - Business logic separation
- **Exception Handling** - Custom exception management
- **Model Pattern** - Domain entities and business objects

## 📁 Project Structure

```
upi/
├── demo.py                           # Comprehensive demo showcasing all patterns
├── upi_app.py                        # Facade implementation
├── app/
│   ├── models/                       # Domain models
│   │   ├── user.py                   # User model with observer implementation
│   │   ├── account.py                # Account model with observer pattern
│   │   ├── payment.py                # Payment model with observer and timer
│   │   ├── transaction.py            # Transaction model with state management
│   │   ├── npci_instance.py          # NPCI singleton for payment processing
│   │   └── enums.py                  # Enums for payment methods, status, etc.
│   ├── services/                     # Business logic layer
│   │   └── payment_service.py        # Payment processing service
│   ├── repositories/                 # Data access layer
│   │   ├── user_respository.py       # User data repository
│   │   └── account_repository.py     # Account data repository
│   ├── observers/                    # Observer pattern implementation
│   │   ├── payment_observer.py       # Payment status change observers
│   │   ├── transaction_observer.py   # Transaction status observers
│   │   └── account_observer.py       # Account balance change observers
│   ├── states/                       # State pattern implementation
│   │   └── transaction_state.py      # Transaction state management
│   ├── strategies/                   # Strategy pattern implementation
│   │   └── payment_strategies.py     # Payment method strategies
│   ├── decorators/                   # Decorator pattern implementation
│   │   ├── base_decorator.py         # Base decorator interface
│   │   ├── fraud_check_decorator.py  # Fraud detection decorator
│   │   └── payment_processor_impl.py # Concrete payment processor
│   ├── proxies/                      # Proxy pattern implementation
│   │   ├── base_proxy.py             # Base proxy interface
│   │   ├── rate_limit_proxy.py       # Rate limiting proxy
│   │   └── secure_bank_proxy.py      # Security proxy
│   ├── chain/                        # Chain of Responsibility implementation
│   │   ├── base_handler.py           # Base handler interface
│   │   ├── chain_factory.py          # Chain factory for creating processing chains
│   │   ├── validation_handler.py     # Payment validation handler
│   │   ├── authentication_handler.py # Authentication handler
│   │   ├── fraud_handler.py          # Fraud detection handler
│   │   ├── routing_handler.py        # Payment routing handler
│   │   └── settlement_handler.py     # Settlement handler
│   ├── commands/                     # Command pattern implementation
│   │   ├── base_command.py           # Base command interface
│   │   ├── command_invoker.py        # Command invoker with retry logic
│   │   └── payment_commands.py       # Payment operation commands
│   ├── abstract_factories/           # Abstract Factory pattern
│   │   ├── abstract_bank_factory.py  # Bank factory interface
│   │   ├── abstract_products.py      # Bank product interfaces
│   │   ├── concrete_bank_factories.py # Concrete bank factories
│   │   ├── hdfc_products.py          # HDFC bank products
│   │   └── sbi_products.py           # SBI bank products
│   ├── adapters/                     # Adapter pattern implementation
│   │   ├── base_adapter.py           # Base adapter interface
│   │   ├── bank_adapter.py           # Bank API adapters
│   │   └── upi_adapter.py            # UPI/NPCI adapter
│   └── exceptions/                   # Exception handling
│       └── insufficient_fund.py      # Custom exception classes
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Setup Instructions

1. **Navigate to the UPI directory**

   ```bash
   cd low_level_design/upi
   ```

2. **Activate virtual environment**

   ```bash
   source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate
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

The demo includes comprehensive sections:

1. **Cross-Bank Transfer Demo** - HDFC to SBI money transfers using Abstract Factory and Adapter patterns
2. **Money Request Demo** - UPI Pull requests between users
3. **Credit Card Payment Demo** - Credit card payments using Strategy pattern
4. **Fraud Detection Demo** - High-value and rapid transaction detection using Decorator pattern
5. **Transaction States Demo** - State pattern for transaction lifecycle management
6. **Chain Processing Demo** - Chain of Responsibility for payment processing
7. **Observers Demo** - Real-time notifications using Observer pattern
8. **Proxies & Decorators Demo** - Access control and security layers
9. **Exception Handling Demo** - Custom exception management
10. **Account Observer Demo** - Account balance change notifications
11. **UPI Adapter Demo** - UPI/NPCI integration demonstration

### Key Features Demonstrated

- **Cross-Bank Transfers**: Seamless money transfers between HDFC and SBI banks
- **Rate Limiting**: Per-user rate limiting (5 requests per minute)
- **Fraud Detection**: Advanced fraud detection with multiple checks
- **Real-time Notifications**: Observer pattern delivers instant updates
- **Multiple Payment Methods**: UPI, Credit Card, Debit Card, Net Banking, Wallet
- **State Management**: Transaction status follows proper state transitions
- **Error Handling**: Comprehensive validation and exception management
- **Security**: Proxy pattern for access control and authentication

## 🔄 Data Flow

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FACADE LAYER                             │
│                    UPIApp (Facade)                          │
│         (Simplified interface for all operations)           │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                   SERVICE LAYER                             │
│                PaymentService                               │
│              (Business Logic)                               │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                 REPOSITORY LAYER                            │
│ UserRepository │ AccountRepository │ (Data Access)          │
│         (Thread-safe operations)                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                   DOMAIN LAYER                              │
│ Models, States, Strategies, Observers, Decorators, Proxies  │
│              (Business Entities & Behaviors)                │
└─────────────────────────────────────────────────────────────┘
```

### Payment Processing Flow

```
User Request → UPIApp (Facade) → Rate Limiting (Proxy) → Payment Chain
     ↓
Validation → Authentication → Fraud Detection → Routing → Settlement
     ↓
Observer Notifications → Real-time Updates → User Notifications
```

### Cross-Bank Transfer Flow

```
UPIApp → PaymentService → Chain of Responsibility → Bank Adapters
     ↓
HDFC Adapter ↔ SBI Adapter → Abstract Factory → Bank Products
     ↓
NPCI Processing → Settlement → Observer Notifications
```

### Fraud Detection Flow

```
Payment Request → Fraud Decorator → Multiple Fraud Checks
     ↓
Velocity Check → Amount Check → Pattern Analysis → Risk Assessment
     ↓
Block/Allow Decision → Observer Notification → Audit Trail
```

### Observer Pattern Flow

```
Event Trigger (Payment/Transaction/Account Change) → Subject
     ↓
notify_observers() → Observer List → Individual Observer.update()
     ↓
Notification Creation → Real-time Display → User Updates
```

## 🏗️ Architecture

### Design Patterns

#### Facade Pattern

- `UPIApp` provides simplified interface to complex payment system
- Hides internal complexity of payment processing
- Single entry point for all payment operations

#### Abstract Factory Pattern

- `HDFCFactory` and `SBIFactory` create bank-specific components
- Connectors, auth handlers, formatters, notifiers
- Easy to add new banks without modifying existing code

#### Adapter Pattern

- `HDFCAdapter`, `SBIAdapter`, `UPIAdapter` standardize bank APIs
- Converts different bank response formats to common interface
- Seamless integration with multiple banks

#### Chain of Responsibility Pattern

- Sequential payment processing: Validation → Authentication → Fraud → Routing → Settlement
- Each handler has specific responsibility
- Easy to add/remove processing steps

#### Command Pattern

- `SendMoneyCommand`, `RequestMoneyCommand`, `ExecutePaymentCommand`
- Encapsulates payment operations
- Supports undo/redo functionality
- `CommandInvoker` manages command execution with retry logic

#### Decorator Pattern

- `FraudCheckDecorator` enhances payment processing
- Adds fraud detection without modifying core logic
- Composable and flexible enhancement system

#### Observer Pattern

- Real-time notifications for payment, transaction, and account changes
- `PaymentObserver`, `TransactionObserver`, `AccountObserver`
- Decoupled notification system
- Automatic event propagation

#### Proxy Pattern

- `RateLimitProxy` for access control and rate limiting
- `SecureBankProxy` for authentication and security
- Controls access to sensitive operations

#### Strategy Pattern

- Different payment methods: `UPIPushStrategy`, `CreditCardStrategy`, `UPIPullStrategy`
- Runtime payment method selection
- Easy to add new payment strategies

#### State Pattern

- Transaction lifecycle management: `PendingState`, `SuccessState`, `FailedState`
- Proper state transitions with validation
- State-specific behavior changes

#### Repository Pattern

- Clean data access layer
- `UserRepository`, `AccountRepository`
- Separation of data access concerns

#### Service Pattern

- Business logic encapsulation
- `PaymentService` handles payment processing
- Clean API interfaces

### Security & Rate Limiting

- **Rate Limiting**: 5 requests per minute per user
- **Fraud Detection**: Multiple fraud checks with configurable thresholds
- **Access Control**: Proxy pattern for security layers
- **Authentication**: Secure bank proxy for user authentication
- **Transaction Monitoring**: Real-time fraud pattern detection

## 📊 Performance Metrics

The system demonstrates excellent performance characteristics:

- **User Registration**: Instant user and account creation
- **Cross-Bank Transfers**: Seamless HDFC ↔ SBI transfers
- **Rate Limiting**: Effective abuse prevention
- **Fraud Detection**: Real-time suspicious transaction detection
- **Observer Notifications**: Instant real-time updates
- **Payment Processing**: Efficient chain-based processing

## 🧪 Testing

The demo includes comprehensive testing covering:

- **Cross-Bank Transfers**: HDFC to SBI money transfers
- **Multiple Payment Methods**: UPI, Credit Card, Money Request
- **Fraud Detection**: High-value and rapid transaction testing
- **Rate Limiting**: Abuse prevention validation
- **Observer Pattern**: Real-time notification testing
- **State Management**: Transaction state transition testing
- **Error Handling**: Exception management validation
- **Bank Integration**: Abstract Factory and Adapter testing

## 🔧 Configuration

### Rate Limiting Configuration

```python
self.rate_limits = {"per_minute": 5, "per_hour": 50}
```

### Fraud Detection Thresholds

```python
self.MAX_DAILY_AMOUNT = 100000.0  # ₹1 lakh per day
self.MAX_HOURLY_TRANSACTIONS = 10  # 10 transactions per hour
self.SUSPICIOUS_AMOUNT_THRESHOLD = 50000.0  # ₹50k single transaction
```

### Payment Expiry

```python
self.expiry_time = self.created_at + timedelta(seconds=3)  # 3 seconds
```

## 📈 Scalability

The system is designed for scalability:

- **Horizontal Scaling**: Repository pattern allows database distribution
- **Vertical Scaling**: Efficient algorithms and data structures
- **Caching**: Observer pattern enables efficient notification caching
- **Load Balancing**: Stateless service design supports load balancing
- **Bank Integration**: Abstract Factory allows easy addition of new banks

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

- **Design Patterns**: Facade, Abstract Factory, Adapter, Chain of Responsibility, Command, Decorator, Observer, Proxy, Strategy, State, Repository, Service, Exception Handling, Model
- **Architecture**: Clean separation of concerns, layered architecture
- **Bank Integration**: Real-world payment system architecture
- **Security**: Rate limiting, fraud detection, access control
- **Real-time Systems**: Observer pattern for instant notifications
- **Error Handling**: Comprehensive exception management
- **Best Practices**: Clean code, proper abstraction, extensibility

## 🔍 Code Quality

- **Type Hints**: Full type annotation support
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Proper exception management
- **Validation**: Input validation and data integrity checks
- **Clean Code**: Readable, maintainable, and well-structured
- **Design Patterns**: Proper implementation of all patterns

## 🌟 Key Features Showcased

### Real-world Scenarios

- Complete UPI payment workflow from registration to settlement
- Cross-bank money transfers (HDFC ↔ SBI)
- Comprehensive fraud detection and prevention
- Rate limiting and abuse prevention
- Real-time payment and transaction notifications
- Multiple payment method support

### Design Pattern Integration

- 14 design patterns working together seamlessly
- Clean separation of concerns
- Extensible and maintainable architecture
- Real-time notification system
- Comprehensive error handling

## 🚀 Advanced Features

### Fraud Detection System

- **Velocity Checks**: Rapid transaction detection
- **Amount Thresholds**: High-value transaction monitoring
- **Pattern Analysis**: Suspicious behavior detection
- **Real-time Blocking**: Instant fraud prevention
- **Audit Trail**: Complete transaction history

### Rate Limiting System

- **Per-user Limits**: Individual rate limiting
- **Time-based Windows**: Per-minute and per-hour limits
- **Automatic Cleanup**: Memory-efficient request tracking
- **Configurable Thresholds**: Easy limit adjustment

### Cross-Bank Integration

- **Abstract Factory**: Bank-specific component creation
- **Adapter Pattern**: Standardized bank communication
- **NPCI Integration**: Real UPI-like processing
- **Settlement Handling**: Inter-bank money movement

### Real-time Notifications

- **Observer Pattern**: Decoupled notification system
- **Multiple Observers**: Payment, Transaction, Account observers
- **Instant Updates**: Real-time status changes
- **Event Propagation**: Automatic notification delivery

### Transaction Management

- **State Pattern**: Proper transaction lifecycle
- **Timeout Management**: Automatic payment expiry
- **Command Pattern**: Undo/redo capabilities
- **Audit Trail**: Complete transaction history

---

**Note**: This is a demonstration project showcasing design patterns and architectural principles. For production use, additional considerations like database persistence, authentication security, API endpoints, payment gateway integration, and regulatory compliance would be required.
