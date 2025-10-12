# UPI Payment System

A comprehensive UPI (Unified Payments Interface) payment system implementation demonstrating various design patterns and architectural principles. This project showcases a complete end-to-end payment processing system with **concurrent transactions**, **real money transfers**, **fraud detection**, **cross-bank transfers**, and **automatic payment expiration**.

## 🚀 Features

### Core Functionality

- **👥 User Management** - Complete user registration and account management with Indian names
- **💰 Real Money Transfers** - Actual balance changes with money conservation
- **🏦 Cross-Bank Transfers** - Seamless transfers between HDFC, SBI, and ICICI banks
- **💳 Multiple Payment Methods** - UPI Push/Pull, Credit Card, Debit Card, Net Banking
- **🛡️ Fraud Detection** - Advanced fraud detection with ₹50,000+ threshold monitoring
- **⚡ Concurrent Transactions** - ThreadPoolExecutor for multi-user simultaneous transactions
- **🔒 Thread Safety** - Data consistency maintained across multiple threads
- **⏰ Automatic Payment Expiration** - Payments expire and notify users automatically
- **📊 Transaction History** - Complete transaction statements and balance tracking
- **🔒 Security** - Proxy pattern for access control and rate limiting
- **🎯 Money Conservation** - Total money in system remains constant across all transactions

### Design Patterns Implemented

- **🏗️ Facade Pattern** - UPIApp provides simplified interface to complex system
- **🏭 Abstract Factory Pattern** - Bank-specific component creation (HDFC, SBI, ICICI)
- **🔌 Adapter Pattern** - Standardized bank API communication with decorators
- **🔗 Chain of Responsibility** - Sequential payment processing pipeline
- **⚡ Command Pattern** - Payment operations with undo/redo capabilities
- **🎨 Decorator Pattern** - Enhanced bank adapters with logging and validation
- **👀 Observer Pattern** - Real-time notifications for payments and transactions
- **🛡️ Proxy Pattern** - Fraud detection between User App and NPCI
- **📋 Strategy Pattern** - Different payment method implementations
- **🔄 State Pattern** - Transaction lifecycle management
- **🗄️ Repository Pattern** - Clean data access layer
- **⚙️ Service Pattern** - Business logic separation
- **🚨 Exception Handling** - Custom exception management
- **📦 Model Pattern** - Domain entities and business objects
- **🧵 Thread Safety** - Concurrent transaction handling
- **🔒 Data Consistency** - ACID properties maintained

## 📁 Project Structure

```
upi/
├── upi_app_demo.py                   # Clean, comprehensive demo showcasing all patterns
├── upi_app.py                        # Facade implementation with proxy and decorator patterns
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
   python3 upi_app_demo.py
   ```

## 🎯 Usage

### Running the Demo

The `upi_app_demo.py` file contains a clean, comprehensive demonstration of all features:

```bash
python3 upi_app_demo.py
```

### Demo Sections

The demo includes comprehensive sections:

1. **💰 Money Transfer Demo** - Real money transfers with actual balance changes
2. **💸 Insufficient Funds Demo** - Proper error handling for insufficient balance
3. **💳 Payment Methods Demo** - UPI Push/Pull, Credit Card payments
4. **⚡ Command Pattern Demo** - Payment operations with undo/redo functionality
5. **👀 Observer Pattern Demo** - Real-time notifications for transactions
6. **🔗 Chain of Responsibility Demo** - Sequential payment processing pipeline
7. **🔄 State Pattern Demo** - Transaction lifecycle state management
8. **🔄 Simplified Flow Demo** - User App → Proxy → NPCI → Bank (with decorators)
9. **🌍 Real-world Scenarios Demo** - Multiple realistic payment scenarios
10. **🏛️ NPCI Integration Demo** - Direct NPCI calls and refund processing
11. **⚡ Concurrent Transactions Demo** - ThreadPoolExecutor with 10 simultaneous transactions

### Key Features Demonstrated

- **💰 Real Money Transfers**: Actual balance changes with money conservation (₹70,000 total maintained)
- **🏦 Cross-Bank Transfers**: Seamless transfers between HDFC, SBI, and ICICI banks
- **⚡ Concurrent Transactions**: 10 simultaneous transactions with 100% success rate
- **🛡️ Fraud Detection**: Advanced fraud detection with ₹50,000+ threshold monitoring
- **🔒 Thread Safety**: Data consistency maintained across multiple threads
- **⏰ Automatic Payment Expiration**: Payments expire and notify users automatically
- **👀 Real-time Notifications**: Observer pattern delivers instant updates
- **💳 Multiple Payment Methods**: UPI Push/Pull, Credit Card, Debit Card
- **🔄 State Management**: Transaction status follows proper state transitions
- **🚨 Error Handling**: Comprehensive validation and exception management
- **🛡️ Security**: Proxy pattern for access control and rate limiting

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
User Request → UPIApp (Facade) → Fraud Proxy → NPCI → Bank Adapter (with Decorator)
     ↓
Rate Limiting → Fraud Detection → VPA Resolution → Inter-bank Transfer
     ↓
Observer Notifications → Real-time Updates → User Notifications
```

### Cross-Bank Transfer Flow

```
UPIApp → Fraud Proxy → NPCI → Bank Adapters (with Decorators)
     ↓
HDFC Adapter ↔ SBI Adapter ↔ ICICI Adapter → Enhanced Processing
     ↓
Real Money Transfer → Balance Updates → Observer Notifications
```

### Fraud Detection Flow

```
Payment Request → NPCI Proxy → Fraud Detection (₹50,000+ threshold)
     ↓
High-value Check → Suspicious Transaction Logging → Allow with Flag
     ↓
Forward to NPCI → Process Payment → Observer Notifications
```

### Concurrent Transactions Flow

```
ThreadPoolExecutor → Multiple Users → Simultaneous Transactions
     ↓
Thread Safety → Data Consistency → Money Conservation
     ↓
10/10 Success Rate → Real Balance Changes → Observer Notifications
```

### Observer Pattern Flow

```
Event Trigger (Payment/Transaction/Account Change) → Subject
     ↓
notify_observers() → Observer List → Individual Observer.update()
     ↓
Notification Creation → Real-time Display → User Updates
```

## 🎯 Latest Improvements

### ✅ **Concurrent Transaction Testing**

- **ThreadPoolExecutor**: 10 simultaneous transactions with 100% success rate
- **Thread Safety**: Data consistency maintained across multiple threads
- **Money Conservation**: Total money in system remains constant (₹70,000)
- **Real Balance Changes**: Actual account balance updates with proper validation

### ✅ **Simplified Architecture**

- **Clean Flow**: User App → Fraud Proxy → NPCI → Bank Adapter (with decorators)
- **Reduced Verbosity**: Clean, concise demo output focusing on essential information
- **Enhanced Decorators**: Bank adapters with logging and validation
- **Fraud Detection**: ₹50,000+ threshold monitoring with suspicious transaction logging

### ✅ **Real-World Features**

- **Indian User Names**: Rahul Sharma, Priya Patel, Amit Kumar, Kavya Reddy
- **Multiple Banks**: HDFC, SBI, ICICI integration with real account numbers
- **Automatic Payment Expiration**: Payments expire and notify users automatically
- **Cross-Bank Transfers**: Seamless inter-bank money transfers

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
