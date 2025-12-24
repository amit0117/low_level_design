# ATM System

A comprehensive Automated Teller Machine (ATM) system implementation demonstrating various design patterns and architectural principles. This project showcases a complete end-to-end ATM system with card authentication, PIN validation, multiple transaction types, multi-bank support, state management, and real-time notifications.

## 🚀 Features

### Core Functionality

- **Card Authentication** - Secure card insertion and validation
- **PIN Validation** - Secure PIN entry via keypad with bank server verification
- **Balance Inquiry** - Real-time account balance checking
- **Cash Withdrawal** - Secure cash dispensing with validation
- **Cash Deposit** - Deposit money to accounts
- **Money Transfer** - Transfer funds between accounts (intra-bank and inter-bank)
- **Multi-Bank Support** - Support for multiple banks (HDFC, SBI, ICICI) via Adapter pattern
- **State Management** - Complete ATM state lifecycle using State pattern
- **Transaction Notifications** - Real-time notifications to users via Observer pattern
- **Cash Management** - ATM cash dispenser with low cash alerts
- **Thread Safety** - Concurrent transaction handling with data consistency

### Design Patterns Implemented

- **Singleton Pattern** - ATMMachine singleton instance (ensures single ATM machine instance)
- **Template Method Pattern** - Transaction execution flow (validate → authorize → perform → dispense → receipt)
- **State Pattern** - ATM state lifecycle management (Idle → Card Inserted → Authenticated → Transaction Selected → Processing)
- **Observer Pattern** - Transaction notifications to users (both sender and receiver for transfers)
- **Adapter Pattern** - Multi-bank integration (HDFC, SBI, ICICI with different APIs)
- **Factory Pattern** - Transaction creation (Withdrawal, Deposit, Transfer, Balance Inquiry factories)
- **Repository Pattern** - Bank server management and access (Singleton pattern)
- **Service Pattern** - Transaction service layer for business logic

### Domain Entities

| Domain Area        | Key Entities                                                                                                                                      |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ATM & Hardware** | `ATM`, `CardReader`, `Keypad`, `CashDispenser`                                                                                                    |
| **Banking**        | `Account`, `Card`, `User`, `Admin`, `BankServer`, `HDFCBank`, `SBIBank`, `ICICIBank`                                                              |
| **Transactions**   | `Transaction`, `WithdrawalTransaction`, `DepositTransaction`, `TransferTransaction`, `BalanceInquiryTransaction`                                  |
| **States**         | `ATMState`, `IdleState`, `CardInsertedState`, `AuthenticatedState`, `TransactionSelectedState`, `TransactionProcessingState`, `OutOfServiceState` |
| **Adapters**       | `HDFCBankAdapter`, `SBIBankAdapter`, `ICICIBankAdapter`                                                                                           |
| **Services**       | `TransactionService`, `BankRepository`                                                                                                            |
| **Observers**      | `BaseObserver`, `BaseSubject`, `User` (as Observer)                                                                                               |

### Core Entities Overview

#### ATM Domain

- **ATM**: Main ATM machine with state management, card reader, keypad, and cash dispenser
- **CardReader**: Hardware component for reading card information
- **Keypad**: Secure PIN input mechanism using `getpass` for password masking
- **CashDispenser**: Cash management with low cash threshold alerts (Observer pattern)

#### Banking Domain

- **Account**: Bank account with thread-safe balance operations
- **Card**: Card entity with card number, CVV, and expiration date
- **User**: Customer and Admin users (Admin observes cash dispenser for low cash alerts)
- **BankServer**: Abstract interface for bank operations (validate_card, validate_pin, deposit, withdraw, etc.)
- **HDFCBank/SBIBank/ICICIBank**: Mock bank implementations with different APIs

#### Transaction Domain

- **Transaction**: Abstract base class implementing Template Method pattern
  - `validate()` → `authorize()` → `perform_transaction()` → `dispense_or_accept()` → `print_receipt()`
  - Observer pattern: Notifies users on transaction completion
- **WithdrawalTransaction**: Cash withdrawal with cash dispenser validation
- **DepositTransaction**: Cash deposit transaction
- **TransferTransaction**: Inter-bank and intra-bank transfers (both sender and receiver notified)
- **BalanceInquiryTransaction**: Account balance inquiry

#### State Domain

- **ATMState**: Abstract base for ATM states
- **IdleState**: Initial state, accepts card insertion
- **CardInsertedState**: Card inserted, accepts PIN entry
- **AuthenticatedState**: PIN validated, accepts transaction selection
- **TransactionSelectedState**: Transaction selected, ready to perform
- **TransactionProcessingState**: Transaction in progress, blocks other operations
- **OutOfServiceState**: ATM out of service

#### Adapter Domain

- **BankServer**: Common interface for all banks
- **HDFCBankAdapter**: Adapts HDFC proprietary API to BankServer interface
- **SBIBankAdapter**: Adapts SBI proprietary API to BankServer interface
- **ICICIBankAdapter**: Adapts ICICI proprietary API to BankServer interface

## 📁 Project Structure

```
atm/
├── atm_machine.py              # Main ATM setup and operations manager
├── demo.py                     # Comprehensive demo with all test scenarios
├── app/
│   ├── models/                 # Domain models
│   │   ├── atm.py              # ATM model with state management
│   │   ├── account.py          # Account model with thread-safe operations
│   │   ├── card.py             # Card model
│   │   ├── card_reader.py      # Card reader hardware component
│   │   ├── keypad.py           # Keypad for secure PIN input
│   │   ├── cash_dispenser.py  # Cash dispenser with observer pattern
│   │   ├── user.py             # User model (Customer and Admin)
│   │   ├── bank_server.py      # Abstract bank server interface
│   │   ├── banks/              # Mock bank implementations
│   │   │   ├── hdfc_bank.py    # HDFC bank with proprietary API
│   │   │   ├── sbi_bank.py     # SBI bank with proprietary API
│   │   │   └── icici_bank.py   # ICICI bank with proprietary API
│   │   ├── transactions/       # Transaction implementations
│   │   │   ├── transaction.py # Abstract transaction base (Template Method)
│   │   │   ├── withdrawal_transaction.py
│   │   │   ├── deposit_transaction.py
│   │   │   ├── transfer_transaction.py
│   │   │   └── balance_inquiry_transaction.py
│   │   └── enums.py            # Enum definitions
│   ├── states/                 # State pattern implementation
│   │   ├── atm_state.py        # Abstract ATM state
│   │   ├── idle_state.py       # Idle state
│   │   ├── card_inserted_state.py
│   │   ├── authenticated_state.py
│   │   ├── transaction_selected_state.py
│   │   ├── transaction_processing_state.py
│   │   └── out_of_service_state.py
│   ├── adapters/               # Adapter pattern implementation
│   │   ├── hdfc_bank_adapter.py
│   │   ├── sbi_bank_adapter.py
│   │   └── icici_bank_adapter.py
│   ├── factories/              # Factory pattern implementation
│   │   └── transaction_factory.py
│   ├── repositories/            # Repository pattern
│   │   └── bank_repository.py  # Bank server repository (Singleton)
│   ├── services/               # Service pattern
│   │   └── transaction_service.py
│   ├── observers/               # Observer pattern
│   │   ├── base_observer.py    # Observer interface
│   │   └── subjects.py         # Subject base class
│   └── exceptions/              # Custom exceptions
│       └── insufficient_money.py
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Setup Instructions

1. **Navigate to the ATM directory**

   ```bash
   cd low_level_design/atm
   ```

2. **Create and activate virtual environment** (optional but recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
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

The demo includes the following test scenarios:

#### 1. Basic Transaction Types

- **Balance Inquiry**: Check account balance with authentication
- **Withdrawal**: Withdraw cash with validation
- **Deposit**: Deposit cash to account
- **Transfer (Same Bank)**: Transfer money between accounts in same bank

#### 2. Inter-Bank Transfer

- Transfer money from HDFC account to SBI account
- Demonstrates cross-bank transaction handling via Adapter pattern
- Shows balances before and after transfer

#### 3. Multiple Simultaneous Transactions

- Tests 5 concurrent transactions on the same account:
  - 2 withdrawals (₹2000, ₹1500)
  - 1 deposit (₹3000)
  - 2 balance inquiries
- Demonstrates thread-safety with concurrent access to the same account
- Uses `threading.Thread` for concurrent execution

#### 4. Insufficient Funds Transfer

- Tests transfer when source account has insufficient funds
- Attempts to transfer more money than available
- Properly handles `InsufficientFundsException`

#### 5. Insufficient Cash in ATM

- Tests withdrawal when ATM doesn't have enough cash
- Attempts to withdraw more than ATM has available
- Properly handles `InsufficientCashException`

### Key Features Demonstrated

- **State Pattern**: Complete ATM state lifecycle management
- **Observer Pattern**: Users notified when their transactions complete
- **Adapter Pattern**: Different bank servers work seamlessly
- **Template Method Pattern**: Consistent transaction execution flow
- **Thread Safety**: Multiple concurrent transactions on same account
- **Error Handling**: Proper exception handling for edge cases

## 📊 Entity Relationship Diagram

### Core Entities and Relationships

```
┌─────────────────────────────────────┐
│          ATMMachine                 │
│─────────────────────────────────────│
│ atm_id                              │
│ current_state (ATMState)            │
│ card_reader (CardReader)            │
│ keypad (Keypad)                     │
│ cash_dispenser (CashDispenser)      │
│ bank_repository (BankRepository)    │
└──────┬──────────────────────────────┘
       │
       │ 1..* (processes)
       │
       ▼
┌─────────────────────────────────────┐
│            Transaction              │
│─────────────────────────────────────│
│ transaction_id                      │
│ account (Account)                   │
│ amount                              │
│ transaction_type                    │
│ status                              │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────────────┐
│ Withdrawal  │ │  Deposit    │ │  Transfer   │ │BalanceInquiry│
└─────────────┘ └─────────────┘ └─────────────┘ └──────────────┘

┌─────────────────────────────────────┐
│            Account                  │
│─────────────────────────────────────│
│ account_number                      │
│ balance                             │
│ account_holder (User)               │
│ bank (BankServer)                   │
└──────┬──────────────────────────────┘
       │
       │ 1..* (has)
       │
       ▼
┌─────────────────────────────────────┐
│             Card                    │
│─────────────────────────────────────│
│ card_number                         │
│ cvv                                 │
│ expiration_date                     │
│ account (Account)                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│             User                    │
│─────────────────────────────────────│
│ user_id                             │
│ name                                │
│ email                               │
│ cards (List<Card>)                  │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┐
       ▼              ▼
┌─────────────┐  ┌─────────────┐
│  Customer   │  │    Admin    │
└─────────────┘  └─────────────┘

┌─────────────────────────────────────┐
│          ATMState                   │
│─────────────────────────────────────│
│ (Abstract)                          │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┬──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ IdleState   │ │CardInserted │ │Authenticated│ │Transaction  │ │OutOfService │
│             │ │   State     │ │   State     │ │SelectedState│ │   State     │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘

┌─────────────────────────────────────┐
│         BankServer                  │
│─────────────────────────────────────│
│ (Abstract Interface)                │
└──────┬──────────────────────────────┘
       │
       │ Implementation via Adapter
       │
       ├──────────────┬──────────────┬
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│HDFCBank     │ │SBIBank      │ │ICICIBank    │
│Adapter      │ │Adapter      │ │Adapter      │
└─────────────┘ └─────────────┘ └─────────────┘

┌─────────────────────────────────────┐
│        CashDispenser                │
│─────────────────────────────────────│
│ cash_available                      │
│ low_cash_threshold                  │
│ observers (List<Observer>)          │
└─────────────────────────────────────┘
```

### Entity Relationships

1. **ATMMachine ↔ ATMState** (One-to-One)

   - ATMMachine has one current_state
   - State transitions: Idle → CardInserted → Authenticated → TransactionSelected → Processing

2. **ATMMachine ↔ Transaction** (One-to-Many)

   - ATMMachine processes multiple Transactions
   - Each Transaction is processed by one ATMMachine

3. **Transaction ↔ Account** (Many-to-One)

   - A Transaction is associated with one Account
   - An Account can have multiple Transactions

4. **Account ↔ Card** (One-to-Many)

   - An Account can have multiple Cards
   - Each Card belongs to one Account

5. **User ↔ Account** (One-to-Many)

   - A User can have multiple Accounts
   - An Account belongs to one User (account_holder)

6. **User ↔ Card** (One-to-Many)

   - A User can have multiple Cards
   - Each Card belongs to one User

7. **User Inheritance Hierarchy**

   - `User` (base class)
   - `Customer`, `Admin` (subclasses)
   - Admin observes CashDispenser for low cash alerts

8. **Transaction Inheritance Hierarchy**

   - `Transaction` (base class, Template Method pattern)
   - `WithdrawalTransaction`, `DepositTransaction`, `TransferTransaction`, `BalanceInquiryTransaction` (subclasses)

9. **ATMState Inheritance Hierarchy**

   - `ATMState` (abstract base)
   - `IdleState`, `CardInsertedState`, `AuthenticatedState`, `TransactionSelectedState`, `TransactionProcessingState`, `OutOfServiceState` (concrete states)

10. **BankServer ↔ Bank Adapters** (Adapter Pattern)

    - `BankServer` is the common interface
    - `HDFCBankAdapter`, `SBIBankAdapter`, `ICICIBankAdapter` adapt different bank APIs

11. **CashDispenser ↔ Observer** (Observer Pattern)

    - CashDispenser notifies observers (Admin) when cash is low
    - Admin implements Observer interface

12. **Transaction ↔ Observer** (Observer Pattern)
    - Transaction notifies observers (Users) on completion
    - Both sender and receiver notified for Transfer transactions

## 🔄 Data Flow

### System Architecture Overview

```
┌───────────────────────────────────────────────────────────------┐
│                    ATM MACHINE LAYER                            │
│              ATMMachine (Setup & Operations)                    │
│         (Bank setup, User management, Transaction orchestration)│
└─────────────────────┬───────────────────────────────────────----┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                   SERVICE LAYER                             │
│              TransactionService                             │
│         (Business Logic - Transaction orchestration)        │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                   ATM MODEL LAYER                           │
│         ATM (State Pattern - State transitions)             │
│    CardReader │ Keypad │ CashDispenser (Observer)           │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│              TRANSACTION LAYER                              │
│     Transaction (Template Method Pattern)                   │
│  Withdrawal │ Deposit │ Transfer │ BalanceInquiry           │
│         (Observer Pattern - Notify users)                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                 REPOSITORY LAYER                            │
│            BankRepository (Singleton)                       │
│    (Bank server management and access)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                 ADAPTER LAYER                               │
│      HDFCBankAdapter │ SBIBankAdapter │ ICICIBankAdapter    │
│         (Adapter Pattern - Bank API abstraction)            │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                   BANK LAYER                                │
│       HDFCBank │ SBIBank │ ICICIBank (Mock banks)           │
│         (Different proprietary APIs)                        │
└─────────────────────────────────────────────────────────────┘
```

### Card Insertion Flow

```
User inserts card → ATM.insert_card() → Current State.insert_card()
     ↓
CardInsertedState → Validate card → Set current_card → Change to CardInsertedState
```

### PIN Entry Flow

```
User enters PIN → ATM.enter_pin() → CardInsertedState.enter_pin()
     ↓
Keypad.enter_pin() → Read PIN securely (getpass) → Validate with bank server
     ↓
If valid → Change to AuthenticatedState → Set current_pin
```

### Transaction Execution Flow

```
User selects transaction → ATM.select_transaction() → AuthenticatedState.select_transaction()
     ↓
TransactionSelectedState → TransactionFactory.create_transaction()
     ↓
Transaction.execute() (Template Method):
  1. validate() - Validate card, PIN, amount, balance
  2. authorize() - PIN validation with bank server
  3. perform_transaction() - Execute transaction with bank server
  4. dispense_or_accept() - Physical cash dispensing or acceptance
  5. print_receipt() - Print transaction receipt
  6. notify_observers() - Notify user(s) via Observer pattern
```

### Transfer Transaction Flow

```
Transfer selected → TransferTransaction created
     ↓
Add both sender and receiver as observers
     ↓
Execute transaction:
  1. Validate source account balance
  2. Debit from source account
  3. Credit to destination account
  4. Notify both sender and receiver
```

### Observer Notification Flow

```
Transaction completes → Transaction.notify_observers()
     ↓
For each observer (User):
  User.update(message) → Print notification to user
     ↓
User receives real-time notification about transaction status
```

### Multi-Bank Transaction Flow

```
Transaction request → BankRepository.get_bank_server(bank_name)
     ↓
Get appropriate adapter (HDFC/SBI/ICICI)
     ↓
Adapter translates common BankServer interface to bank-specific API
     ↓
Bank-specific operation executed → Result returned via adapter
```

### State Transition Flow

```
IdleState → Card Inserted → CardInsertedState
     ↓
PIN Entered → AuthenticatedState
     ↓
Transaction Selected → TransactionSelectedState
     ↓
Transaction Processing → TransactionProcessingState
     ↓
Transaction Complete → Eject Card → IdleState
```

## 🏗️ Architecture

### Design Patterns

#### Singleton Pattern

The `ATMMachine` class ensures a single instance across the application:

```python
class ATMMachine:
    _instance: Optional["ATMMachine"] = None
    _lock: Lock = Lock()
    _initialized: bool = False

    def __new__(cls, atm_name: str = "Main ATM", initial_cash: float = 100000.0) -> "ATMMachine":
        """Singleton implementation with thread safety"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._atm_name = atm_name
                    cls._instance._initial_cash = initial_cash
        return cls._instance

    @classmethod
    def get_instance(cls, atm_name: str = "Main ATM", initial_cash: float = 100000.0) -> "ATMMachine":
        """Get the singleton instance of ATMMachine"""
        return cls(atm_name=atm_name, initial_cash=initial_cash)
```

**Benefits**:

- Single ATM machine instance across the application
- Thread-safe implementation with double-checked locking
- Centralized access point for all ATM operations
- Prevents multiple ATM instances from conflicting

**Use Case**: Ensures that only one ATM machine instance exists, maintaining consistency in bank registrations, user management, and transaction handling.

#### Template Method Pattern

The `Transaction` base class defines the skeleton of the transaction algorithm:

```python
class Transaction(ABC, BaseSubject):
    def execute(self):
        self.validate()           # Step 1: Validate inputs
        self.authorize()          # Step 2: Authorize (PIN validation)
        try:
            self.perform_transaction()  # Step 3: Execute transaction
            self.dispense_or_accept()   # Step 4: Physical operation
            self.print_receipt()        # Step 5: Print receipt
            self.notify_observers()     # Step 6: Notify observers
        except Exception as e:
            self.rollback()             # Rollback on failure
```

Each concrete transaction (Withdrawal, Deposit, Transfer, BalanceInquiry) implements the abstract methods, providing specific behavior while maintaining the same execution flow.

**Benefits**:

- Consistent transaction execution across all transaction types
- Easy to add new transaction types
- Centralized error handling and rollback

#### State Pattern

The ATM uses State pattern to manage its operational lifecycle:

- **IdleState**: Initial state, accepts card insertion
- **CardInsertedState**: Card inserted, accepts PIN entry
- **AuthenticatedState**: PIN validated, accepts transaction selection
- **TransactionSelectedState**: Transaction selected, ready to perform
- **TransactionProcessingState**: Transaction in progress
- **OutOfServiceState**: ATM out of service

Each state defines what operations are allowed in that state, preventing invalid operations.

**Benefits**:

- Clear state transitions
- Prevents invalid operations
- Easy to add new states or modify state behavior

#### Observer Pattern

Transactions act as Subjects and Users act as Observers:

- **For transfers**: Both sender and receiver are notified
- **For other transactions**: The user initiating the transaction is notified
- Users receive notifications when transactions complete (success or failure)

```python
class Transaction(BaseSubject):
    def __init__(self):
        # Add relevant users as observers
        user = account.get_user()
        if user:
            self.add_observer(user)

    def execute(self):
        # ... perform transaction ...
        self.notify_observers("Transaction completed successfully")
```

**Benefits**:

- Decoupled notification system
- Real-time user notifications
- Easy to add new notification types

#### Adapter Pattern

Different banks have different APIs. Adapters translate between the common `BankServer` interface and bank-specific APIs:

- **HDFCBankAdapter**: Adapts HDFC proprietary API (`checkBalance`, `debitAmount`, `creditAmount`)
- **SBIBankAdapter**: Adapts SBI proprietary API (`getBalance`, `transferOut`, `transferIn`)
- **ICICIBankAdapter**: Adapts ICICI proprietary API (`balance`, `deduct`, `add`)

```python
class HDFCBankAdapter(BankServer):
    def __init__(self, hdfc_bank: HDFCBank):
        self.hdfc_bank = hdfc_bank

    def get_account_balance(self, account_number: str) -> float:
        # Translate common interface to HDFC API
        return self.hdfc_bank.checkBalance(account_number)
```

**Benefits**:

- ATM works with multiple banks without code changes
- Easy to add new banks
- Maintains clean separation between ATM and bank implementations

#### Factory Pattern

Transaction factories create appropriate transaction objects:

- **WithdrawalTransactionFactory**: Creates withdrawal transactions
- **DepositTransactionFactory**: Creates deposit transactions
- **TransferTransactionFactory**: Creates transfer transactions
- **BalanceInquiryTransactionFactory**: Creates balance inquiry transactions

**Benefits**:

- Centralized transaction creation
- Easy to extend with new transaction types
- Hides transaction creation complexity

#### Repository Pattern

`BankRepository` manages bank server instances (Singleton pattern):

- Stores all bank adapters
- Provides access to bank servers by name
- Ensures single instance across the application

**Benefits**:

- Centralized bank server management
- Easy access to banks
- Single source of truth for bank servers

#### Service Pattern

`TransactionService` provides a high-level interface for transactions:

- Orchestrates ATM state transitions
- Handles transaction execution
- Provides user-friendly error messages
- Abstracts underlying complexity

**Benefits**:

- Clean API for transaction operations
- Centralized business logic
- Easy to test and maintain

### Use Cases for Design Patterns

#### Singleton Pattern

- **Single ATM Instance**: Ensures only one ATM machine instance exists
- **Centralized Management**: All ATM operations go through single instance
- **Resource Efficiency**: Prevents duplicate bank registrations and resource allocation
- **Thread Safety**: Safe concurrent access with double-checked locking

#### Template Method Pattern

- **Transaction Execution**: Ensures all transactions follow the same validation and execution flow
- **Consistency**: All transactions validate, authorize, perform, and notify in the same order
- **Extensibility**: Easy to add new transaction types by implementing abstract methods

#### State Pattern

- **ATM Lifecycle**: Manages complete ATM operational lifecycle
- **Invalid Operation Prevention**: Prevents operations in invalid states (e.g., can't select transaction before PIN entry)
- **State-Specific Behavior**: Each state defines what operations are allowed

#### Observer Pattern

- **Transaction Notifications**: Users notified when transactions complete
- **Transfer Notifications**: Both sender and receiver notified for transfers
- **Low Cash Alerts**: Admins notified when ATM cash is low

#### Adapter Pattern

- **Multi-Bank Support**: ATM works with different banks having different APIs
- **Bank Integration**: Easy integration with new banks
- **API Abstraction**: ATM doesn't need to know bank-specific APIs

## 🧪 Testing

The demo includes comprehensive testing covering:

- **Basic Transactions**: All transaction types (balance inquiry, withdrawal, deposit, transfer)
- **Inter-Bank Transfer**: Cross-bank transactions
- **Multi-User Concurrency**: 5 concurrent transactions on same account
- **Insufficient Funds**: Transfer with insufficient funds handling
- **Insufficient Cash**: Withdrawal when ATM has insufficient cash
- **Observer Pattern**: Transaction notifications verified
- **State Management**: ATM state transitions tested
- **Error Handling**: Invalid operation testing
- **Thread Safety**: Concurrent access validation

### Test Scenarios

1. **Balance Inquiry**: Validates card, PIN, and returns balance
2. **Withdrawal**: Validates balance, ATM cash, and dispenses cash
3. **Deposit**: Accepts deposit and updates account balance
4. **Transfer (Same Bank)**: Transfers money between accounts in same bank
5. **Inter-Bank Transfer**: Transfers money between different banks
6. **Concurrent Transactions**: Multiple threads performing transactions simultaneously
7. **Insufficient Funds**: Proper exception handling when account lacks funds
8. **Insufficient Cash**: Proper exception handling when ATM lacks cash

## 🔧 Configuration

### Environment Variables

No environment variables required for basic operation.

### Customization

- **Add New Banks**: Implement bank-specific adapter extending `BankServer`
- **Add New Transaction Types**: Create transaction class extending `Transaction` and add factory
- **Modify ATM States**: Add new states by extending `ATMState` and updating state transitions
- **Add New Observers**: Extend `BaseObserver` and add to transaction observers

## 📈 Scalability

The system is designed for scalability:

- **Horizontal Scaling**: Repository pattern allows multiple ATM instances
- **Vertical Scaling**: Efficient algorithms and data structures
- **Thread Safety**: Concurrent transaction handling with locks
- **Stateless Services**: Service layer supports load balancing
- **Observer Pattern**: Efficient notification delivery

## 🎓 Learning Objectives

This project demonstrates:

- **Design Patterns**: Template Method, State, Observer, Adapter, Factory, Repository, Service, Singleton
- **Architecture**: Clean separation of concerns, layered architecture
- **Concurrency**: Thread safety, data consistency, race condition prevention
- **Banking Domain**: Real-world ATM system implementation
- **Error Handling**: Comprehensive validation and error management
- **State Management**: Complete state lifecycle management
- **Multi-Bank Integration**: Adapter pattern for integrating multiple banks
- **Real-time Notifications**: Observer pattern for transaction notifications

## 🔍 Code Quality

- **Type Hints**: Full type annotation support
- **Error Handling**: Proper exception management with custom exceptions
- **Validation**: Input validation and data integrity checks
- **Thread Safety**: Concurrent access protection with locks
- **Clean Code**: Readable, maintainable, and well-structured
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion

## 📊 Performance Metrics

The system demonstrates excellent performance characteristics:

- **Transaction Execution**: Fast transaction processing with proper validation
- **Concurrent Operations**: Thread-safe concurrent transaction handling
- **State Transitions**: Efficient state management with minimal overhead
- **Observer Notifications**: Real-time notification delivery
- **Bank Integration**: Fast bank server communication via adapters

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is for educational purposes demonstrating design patterns and architectural principles.

---

**Note**: This is a demonstration project showcasing design patterns and architectural principles. For production use, additional considerations like database persistence, network security, encryption, and real hardware integration would be required.
