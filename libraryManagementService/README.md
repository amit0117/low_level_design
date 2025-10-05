# Library Management Service

A comprehensive library management system implementation demonstrating various design patterns and architectural principles. This project showcases a complete end-to-end library management system with catalog management, member registration, borrowing operations, payment processing, and real-time notifications.

## 🚀 Features

### Core Functionality

- **Librarian Catalog Management** - Add, update, and remove books from library catalog
- **Member Registration & Management** - Complete member profile management with borrowing history
- **Borrowing Operations** - Request, borrow, renew, and return books with rules enforcement
- **Payment Processing** - Multiple payment methods for membership fees and fines
- **Fine Management** - Automated fine calculation and payment processing
- **Item Status Management** - Track item status (available, reserved, issued, damaged, lost)
- **Real-time Notifications** - Observer pattern for item status changes
- **Concurrent Access** - Thread-safe operations with data consistency
- **Comprehensive Reporting** - Detailed library statistics and analytics

### Design Patterns Implemented

- **Singleton Pattern** - Single instance of LibraryManagement system
- **Observer Pattern** - Real-time notifications for item status changes
- **State Pattern** - Item status lifecycle management
- **Strategy Pattern** - Flexible payment processing methods
- **Repository Pattern** - Clean data access layer
- **Service Pattern** - Business logic separation
- **Factory Pattern** - Library item creation
- **Facade Pattern** - Simplified interface to complex subsystem

## 📁 Project Structure

```
libraryManagementService/
├── run.py                          # Main demo file
├── library_management.py           # Facade and Singleton implementation
├── app/
│   ├── models/                     # Domain models
│   │   ├── library_item.py        # Library item model with state management
│   │   ├── member.py              # Member model with observer implementation
│   │   ├── borrow.py              # Borrow model for borrowing operations
│   │   ├── book.py                # Book model (extends LibraryItem)
│   │   ├── magazine.py            # Magazine model (extends LibraryItem)
│   │   ├── payment_result.py      # Payment result model
│   │   └── enums.py               # Enums for status and types
│   ├── services/                  # Business logic layer
│   │   ├── payment_service.py     # Payment processing service
│   │   └── search_service.py      # Search functionality service
│   ├── repositories/              # Data access layer
│   │   ├── item_repository.py     # Item data repository
│   │   ├── member_repository.py  # Member data repository
│   │   └── borrow_repository.py  # Borrow data repository
│   ├── observers/                 # Observer pattern implementation
│   │   └── item_observer.py      # Item status change observers
│   ├── states/                    # State pattern implementation
│   │   └── item_state.py         # Item state management
│   ├── strategies/                # Strategy pattern implementation
│   │   ├── payment_strategy.py   # Payment processing strategies
│   │   └── item_search_strategy.py # Search strategies
│   └── factories/                 # Factory pattern implementation
│       └── library_item_factory.py # Library item creation factory
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd libraryManagementService
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt  # If requirements.txt exists
   ```

4. **Run the demo**
   ```bash
   python run.py
   ```

## 🎯 Usage

### Running the Demo

The `run.py` file contains a comprehensive demonstration of all features:

```bash
python run.py
```

### Demo Sections

The demo includes two main sections:

1. **Complete Library Management Workflow** (9 scenarios)

   - Librarian Catalog Management
   - Member Registration & Management
   - Borrowing Operations & Rules Enforcement
   - Renewal Operations
   - Payment Processing
   - Fine Management
   - Return Operations
   - Item Status Management
   - Comprehensive Reporting

2. **Comprehensive Validation** (7 validation scenarios)
   - Librarian Catalog Management
   - Member Management
   - Borrowing Rules & Enforcement
   - Concurrent Access Testing
   - Payment & Fine Management
   - Advanced Features
   - Performance & Scalability

### Key Features Demonstrated

- **Thread Safety**: Singleton pattern ensures single instance across threads
- **Real-time Notifications**: Observer pattern delivers instant item status updates
- **Data Consistency**: Thread-safe operations prevent race conditions
- **State Management**: Item status follows proper state transitions
- **Payment Processing**: Multiple payment methods with strategy pattern
- **Error Handling**: Comprehensive validation and error management

## 🔄 Data Flow

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FACADE LAYER                             │
│              LibraryManagement (Singleton)                  │
│         (Simplified interface for all operations)           │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                   SERVICE LAYER                             │
│  PaymentService  │  SearchService  │  (Business Logic)      │
│  (Payment processing, Search functionality)                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                 REPOSITORY LAYER                            │
│ ItemRepository │ MemberRepository │ BorrowRepository        │
│         (Data Access - Thread-safe operations)              │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                   DOMAIN LAYER                              │
│   Models, States, Strategies, Observers, Factories          │
│              (Business Entities & Behaviors)                │
└─────────────────────────────────────────────────────────────┘
```

### Member Registration Flow

```
User Input → LibraryManagement → MemberRepository → Member Model
     ↓
Profile Creation → Observer Registration → Notification Setup
```

### Book Addition Flow

```
Librarian Input → LibraryManagement → ItemRepository → LibraryItem Model
     ↓
Factory Pattern → Item Creation → State Management → Observer Setup
```

### Borrowing Request Flow

```
Member Request → LibraryManagement → Validation → Borrow Model Creation
     ↓
Item Reservation → State Transition → Observer Notification → Member Notification
```

### Borrowing Process Flow

```
Borrow Request → LibraryManagement → Borrow Model → Item State Change
     ↓
Due Date Calculation → Member History Update → Observer Notification
```

### Return Process Flow

```
Return Request → LibraryManagement → Fine Calculation → Item State Change
     ↓
Item Availability → Member History Update → Observer Notification
```

### Payment Processing Flow

```
Payment Request → PaymentService → Strategy Pattern → Payment Method
     ↓
Payment Processing → PaymentResult → Fine/Membership Update
```

### Item Status Management Flow

```
Status Change → ItemState → State Pattern → Observer Notification
     ↓
Status Update → Item Model → Repository Update → Member Notification
```

### Multi-User Concurrency Flow

```
Multiple Users → ThreadPoolExecutor → Concurrent Operations
     ↓
Singleton Manager → Thread-safe Repositories → Process Locks
     ↓
Data Consistency → Observer Notifications → Real-time Updates
```

### Observer Pattern Data Flow

```
Event Trigger (Item Status Change) → ItemSubject
     ↓
notify_observers() → Observer List → Individual Observer.update()
     ↓
Notification Creation → Member Notification → Real-time Display
```

## 🏗️ Architecture

### Design Patterns

#### Singleton Pattern

- `LibraryManagement` ensures single instance
- Thread-safe implementation with double-checked locking
- Centralized access point for all operations

#### Observer Pattern

- Real-time notifications for item status changes
- Decoupled notification system
- Automatic event propagation to members

#### State Pattern

- Item lifecycle management
- Proper state transitions (Available → Reserved → Issued → Returned)
- Invalid transition prevention

#### Strategy Pattern

- Flexible payment processing methods
- Easy to add new payment strategies
- Runtime payment method selection

#### Repository Pattern

- Clean data access layer
- Thread-safe data operations
- Separation of concerns

#### Service Pattern

- Business logic encapsulation
- Input validation and error handling
- Clean API interfaces

#### Factory Pattern

- Library item creation
- Type-specific item instantiation
- Extensible item types

#### Facade Pattern

- Simplified interface to complex subsystem
- Hides internal complexity
- Unified API for all operations

### Concurrency & Thread Safety

- **Thread-Safe Singletons**: Double-checked locking mechanism
- **Repository Locks**: Process locks for data access operations
- **State Management**: Thread-safe state transitions
- **Observer Notifications**: Thread-safe notification delivery

## 📊 Performance Metrics

The system demonstrates excellent performance characteristics:

- **Member Registration**: 10 members in ~0.000 seconds
- **Book Addition**: 10 books in ~0.000 seconds
- **Report Generation**: Generated in ~0.000 seconds
- **Concurrent Operations**: 5/5 successful with ThreadPoolExecutor
- **Data Consistency**: Zero data corruption under concurrent access

## 🧪 Testing

The demo includes comprehensive testing covering:

- **Multi-User Concurrency**: ThreadPoolExecutor with 5 concurrent operations
- **Data Consistency**: Verification of data integrity under load
- **Observer Pattern**: Real-time notification delivery validation
- **State Management**: Item state transition testing
- **Error Handling**: Invalid operation testing
- **Performance**: Bulk operation timing
- **Borrowing Rules**: Maximum books, renewal limits, loan duration
- **Payment Processing**: Multiple payment methods validation

## 🔧 Configuration

### Environment Variables

No environment variables required for basic operation.

### Customization

- Payment strategies can be easily extended
- Item types can be added through factory pattern
- New item states can be implemented
- Additional member profile fields can be added
- Search strategies can be customized

## 📈 Scalability

The system is designed for scalability:

- **Horizontal Scaling**: Repository pattern allows database distribution
- **Vertical Scaling**: Efficient algorithms and data structures
- **Caching**: Observer pattern enables efficient notification caching
- **Load Balancing**: Stateless service design supports load balancing

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

- **Design Patterns**: Singleton, Observer, State, Strategy, Repository, Service, Factory, Facade
- **Architecture**: Clean separation of concerns, layered architecture
- **Concurrency**: Thread safety, data consistency, race condition prevention
- **Testing**: Comprehensive validation, multi-user scenarios
- **Performance**: Efficient algorithms, scalability considerations
- **Best Practices**: Error handling, validation, documentation

## 🔍 Code Quality

- **Type Hints**: Full type annotation support
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Proper exception management
- **Validation**: Input validation and data integrity checks
- **Thread Safety**: Concurrent access protection
- **Clean Code**: Readable, maintainable, and well-structured

## 🌟 Key Features Showcased

### Indian Context

- Uses Indian names throughout the demo (Arjun Sharma, Priya Patel, Rajesh Kumar, etc.)
- Indian authors and books in bulk operations
- Indian bank names (State Bank of India, HDFC Bank)

### Real-world Scenarios

- Complete library workflow from registration to reporting
- Comprehensive error handling and validation
- Multi-user concurrent access simulation
- Performance and scalability testing

### Design Pattern Integration

- Multiple patterns working together seamlessly
- Clean separation of concerns
- Extensible and maintainable architecture
- Thread-safe concurrent operations

---

**Note**: This is a demonstration project showcasing design patterns and architectural principles. For production use, additional considerations like database persistence, authentication security, and API endpoints would be required.
