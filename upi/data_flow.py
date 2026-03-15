"""
Mermaid Diagrams for UPI (Unified Payments Interface) - Low Level Design
"""

DATA_FLOW_DIAGRAM = """
```mermaid
graph TD
    User[User] -->|has| Account[Account Subject]
    Account -->|stored in| AccountRepo[AccountRepository]
    User -->|stored in| UserRepo[UserRepository]
    Account -->|observed by| AccountObserver[AccountObserver]

    User -->|initiates| Payment[Payment]
    Payment -->|executed via| CommandInvoker[CommandInvoker]
    CommandInvoker -->|executes| Command{Command}
    Command -->|execute| ExecutePaymentCommand[ExecutePaymentCommand]

    Payment -->|processed by| PaymentProcessor[PaymentProcessor]
    PaymentProcessor -->|validates through| HandlerChain{Payment Handler Chain}
    HandlerChain -->|1| AuthHandler[AuthenticationHandler]
    HandlerChain -->|2| FraudHandler[FraudHandler]
    HandlerChain -->|3| ValidationHandler[ValidationHandler]
    HandlerChain -->|4| SettlementHandler[SettlementHandler]
    HandlerChain -->|5| RoutingHandler[RoutingHandler]

    AuthHandler -->|next| FraudHandler
    FraudHandler -->|next| ValidationHandler
    ValidationHandler -->|next| SettlementHandler
    SettlementHandler -->|next| RoutingHandler

    RoutingHandler -->|routes to| BankAdapter{BankAPI Adapter}
    BankAdapter -->|decorated by| FraudCheckDecorator[FraudCheckDecorator]
    BankAdapter -->|created by| BankFactory{Bank Integration Factory}
    BankFactory -->|HDFC| HDFCFactory[HDFCFactory]
    BankFactory -->|SBI| SBIFactory[SBIFactory]

    Payment -->|uses| PaymentStrategy{Payment Strategy}
    PaymentStrategy -->|credit card| CreditCard[CreditCardStrategy]
    PaymentStrategy -->|debit card| DebitCard[DebitCardStrategy]

    Payment -->|routed via| NPCI[NPCI]
    Payment -->|creates| Transaction[Transaction]
    Transaction -->|has| TransactionState{Transaction State}
    TransactionState -->|cancelled| CancelledState[CancelledState]
    TransactionState -->|failed| FailedState[FailedState]

    Account -->|notified by| AccountObserver
```
"""

USER_FLOW_DIAGRAM = """
```mermaid
sequenceDiagram
    actor Sender as Sender (User)
    actor Receiver as Receiver (User)
    participant CommandInvoker
    participant PaymentProcessor
    participant AuthHandler as AuthenticationHandler
    participant FraudHandler as FraudHandler
    participant Validator as ValidationHandler
    participant Settlement as SettlementHandler
    participant Router as RoutingHandler
    participant NPCI
    participant BankAdapter as BankAPIAdapter
    participant Transaction

    Sender->>CommandInvoker: Initiate payment (amount, receiver VPA)
    CommandInvoker->>CommandInvoker: Create ExecutePaymentCommand

    CommandInvoker->>PaymentProcessor: Execute payment
    PaymentProcessor->>AuthHandler: Step 1 - Authenticate
    AuthHandler->>AuthHandler: Verify sender account & PIN
    AuthHandler-->>PaymentProcessor: Auth passed

    PaymentProcessor->>FraudHandler: Step 2 - Fraud check
    FraudHandler->>FraudHandler: Check suspicious patterns
    FraudHandler-->>PaymentProcessor: No fraud detected

    PaymentProcessor->>Validator: Step 3 - Validate
    Validator->>Validator: Check sufficient funds
    Validator->>Validator: Validate transaction limits
    Validator-->>PaymentProcessor: Validation passed

    PaymentProcessor->>Settlement: Step 4 - Settle
    Settlement->>Settlement: Debit sender account
    Settlement->>Settlement: Credit receiver account
    Settlement-->>PaymentProcessor: Settlement done

    PaymentProcessor->>Router: Step 5 - Route
    Router->>NPCI: Route through NPCI
    NPCI->>BankAdapter: Forward to receiver's bank
    BankAdapter->>BankAdapter: Process via bank (HDFC/SBI)
    BankAdapter-->>NPCI: Bank confirmation
    NPCI-->>Router: Transaction confirmed

    Router->>Transaction: Create transaction record
    Note over Transaction: State = SUCCESS

    Transaction-->>Sender: Payment successful notification
    Transaction-->>Receiver: Payment received notification

    Note over Sender: Undo support via Command pattern
    Sender->>CommandInvoker: Undo last payment (if supported)
    CommandInvoker->>CommandInvoker: Reverse ExecutePaymentCommand
```
"""

if __name__ == "__main__":
    print("=" * 60)
    print("DATA FLOW DIAGRAM")
    print("=" * 60)
    print(DATA_FLOW_DIAGRAM)
    print("=" * 60)
    print("USER FLOW DIAGRAM")
    print("=" * 60)
    print(USER_FLOW_DIAGRAM)
