"""
Mermaid Diagrams for Splitwise - Low Level Design
"""

DATA_FLOW_DIAGRAM = """
```mermaid
graph TD
    User[User] -->|creates/joins| Group[Group]
    User -->|managed by| GroupManager[GroupManager]

    Group -->|has many| Expense[Expense]
    Expense -->|managed by| ExpenseManager[ExpenseManager]
    Expense -->|paid by| Payer[Payer/User]
    Expense -->|split among| Participants[Participants/Users]

    Expense -->|uses| SplitStrategy{Split Strategy}
    SplitStrategy -->|equal| EqualSplit[EqualSplit]
    SplitStrategy -->|exact| ExactSplit[ExactSplit]
    SplitStrategy -->|percentage| PercentageSplit[PercentageSplit]

    SplitStrategy -->|calculates| IndividualShare[Individual Shares]
    IndividualShare -->|updates| Balance[Balance]
    Balance -->|tracks| OwedAmounts[Who owes whom]

    Balance -->|settled via| SettlementService[SettlementService]
    SettlementService -->|creates| Transaction[Transaction]
    Transaction -->|from| Debtor[Debtor/User]
    Transaction -->|to| Creditor[Creditor/User]
    Transaction -->|updates| Balance
```
"""

USER_FLOW_DIAGRAM = """
```mermaid
sequenceDiagram
    actor User1 as User A (Payer)
    actor User2 as User B
    actor User3 as User C
    participant GroupManager
    participant Group
    participant ExpenseManager
    participant SplitStrategy
    participant Balance
    participant SettlementService

    User1->>GroupManager: Create group "Trip"
    GroupManager->>Group: Initialize group
    User2->>Group: Join group
    User3->>Group: Join group

    User1->>ExpenseManager: Add expense (₹3000 dinner)
    ExpenseManager->>SplitStrategy: Split among 3 users

    alt Equal Split
        SplitStrategy->>SplitStrategy: ₹3000 / 3 = ₹1000 each
    else Exact Split
        SplitStrategy->>SplitStrategy: A=₹1500, B=₹1000, C=₹500
    else Percentage Split
        SplitStrategy->>SplitStrategy: A=50%, B=30%, C=20%
    end

    SplitStrategy->>Balance: Update balances
    Balance-->>User1: User B owes you ₹1000
    Balance-->>User1: User C owes you ₹1000
    Balance-->>User2: You owe User A ₹1000
    Balance-->>User3: You owe User A ₹1000

    Note over User2: More expenses added over time...

    User1->>ExpenseManager: View all balances
    ExpenseManager->>Balance: Calculate net balances
    Balance-->>User1: Net balance summary

    User2->>SettlementService: Settle debt with User A
    SettlementService->>SettlementService: Create transaction (B → A: ₹1000)
    SettlementService->>Balance: Update balance
    Balance-->>User2: Debt settled
    Balance-->>User1: Payment received from User B

    User3->>SettlementService: Settle debt with User A
    SettlementService->>Balance: Update balance
    Balance-->>User3: Debt settled
    Balance-->>User1: All debts cleared
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
