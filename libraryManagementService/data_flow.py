"""
Mermaid Diagrams for Library Management Service - Low Level Design
"""

DATA_FLOW_DIAGRAM = """
```mermaid
graph TD
    Librarian[Librarian] -->|adds items via| ItemFactory{Library Item Factory}
    ItemFactory -->|book| BookFactory[BookFactory]
    ItemFactory -->|magazine| MagazineFactory[MagazineFactory]
    BookFactory -->|creates| Book[Book]
    MagazineFactory -->|creates| Magazine[Magazine]
    Book -->|stored in| ItemRepository[ItemRepository]
    Magazine -->|stored in| ItemRepository

    Book -->|has| ItemState{Item State}
    ItemState -->|available| AvailableState[AvailableState]
    ItemState -->|issued| IssuedState[IssuedState]
    ItemState -->|damaged| DamagedState[DamagedState]
    ItemState -->|lost| LostState[LostState]

    Member[Member] -->|stored in| MemberRepository[MemberRepository]
    Member -->|searches via| SearchService[SearchService]
    SearchService -->|uses| ItemSearchStrategy[ItemSearchStrategy]
    ItemSearchStrategy -->|queries| ItemRepository

    Member -->|borrows| Borrow[Borrow]
    Borrow -->|links| Book
    Borrow -->|has| BorrowStatus[BorrowStatus]
    Borrow -->|stored in| BorrowRepository[BorrowRepository]

    Borrow -->|calculates| Fine[Fine Amount]
    Fine -->|paid via| PaymentService[PaymentService]
    PaymentService -->|uses| PaymentStrategy{Payment Strategy}
    PaymentStrategy -->|credit card| CreditCard[CreditCardPayment]
    PaymentStrategy -->|cash| Cash[CashPayment]
    PaymentStrategy -->|bank transfer| BankTransfer[BankTransferPayment]

    Member -->|observed by| ItemObserver[ItemObserver]
```
"""

USER_FLOW_DIAGRAM = """
```mermaid
sequenceDiagram
    actor Librarian
    actor Member
    participant ItemFactory
    participant ItemRepo as ItemRepository
    participant SearchService
    participant BorrowRepo as BorrowRepository
    participant PaymentService

    Librarian->>ItemFactory: Create book/magazine
    ItemFactory-->>ItemRepo: Store new item
    Note over ItemRepo: Item State = AvailableState

    Member->>SearchService: Search for item
    SearchService->>ItemRepo: Query by strategy
    ItemRepo-->>SearchService: Matching items
    SearchService-->>Member: Search results

    Member->>BorrowRepo: Borrow item
    BorrowRepo->>ItemRepo: Update item state
    Note over ItemRepo: Item State = IssuedState
    BorrowRepo-->>Member: Borrow receipt with due date

    alt Return on time
        Member->>BorrowRepo: Return item
        BorrowRepo->>ItemRepo: Update item state
        Note over ItemRepo: Item State = AvailableState
        BorrowRepo-->>Member: Return confirmed, no fine
    else Return late
        Member->>BorrowRepo: Return item (overdue)
        BorrowRepo->>BorrowRepo: Calculate fine
        BorrowRepo-->>Member: Fine amount due

        Member->>PaymentService: Pay fine
        PaymentService-->>Member: Payment receipt
        BorrowRepo->>ItemRepo: Update item state
        Note over ItemRepo: Item State = AvailableState
    else Item damaged
        Member->>BorrowRepo: Report damaged
        Note over ItemRepo: Item State = DamagedState
        BorrowRepo-->>Member: Damage fine assessed
        Member->>PaymentService: Pay damage fine
    else Item lost
        Member->>BorrowRepo: Report lost
        Note over ItemRepo: Item State = LostState
        BorrowRepo-->>Member: Replacement fine assessed
        Member->>PaymentService: Pay replacement fine
    end
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
