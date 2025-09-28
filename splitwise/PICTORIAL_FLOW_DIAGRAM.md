# 🎨 Splitwise - Pictorial Flow Diagram

## 📊 Visual System Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🎯 SPLITWISE SYSTEM OVERVIEW                        │
└─────────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────────┐
                    │           🏢 USER ENTERS             │
                    │        SplitWiseService             │
                    │         (Singleton)                 │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │        🔧 FACADE PROCESSES          │
                    │     • UserService                   │
                    │     • GroupService                  │
                    │     • Thread-safe operations        │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │        👥 CREATES DOMAIN            │
                    │     • User (Observer)               │
                    │     • Group (Subject)               │
                    │     • Expense (Subject)             │
                    │     • Transaction (Subject)         │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │        💰 EXPENSE SPLITTING         │
                    │     • EqualSplitStrategy            │
                    │     • PercentSplitStrategy           │
                    │     • ExactSplitStrategy             │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │        🔨 BUILDER CONSTRUCTS        │
                    │     • ExpenseBuilder                │
                    │     • Validation                    │
                    │     • Complex object creation       │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │        📊 BALANCE UPDATES          │
                    │     • BalanceSheet (Thread-safe)   │
                    │     • Real-time calculations        │
                    │     • Concurrent access            │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │        👁️ OBSERVER NOTIFIES         │
                    │     • expense_update()              │
                    │     • transaction_update()          │
                    │     • update_group()                │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │        🧮 DEBT SIMPLIFICATION      │
                    │     • Heap-based algorithm          │
                    │     • Minimize transactions         │
                    │     • Optimal creditor-debtor       │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │        ✅ RESPONSE TO USER          │
                    │     • Updated balances              │
                    │     • Transaction history           │
                    │     • Notifications sent            │
                    └─────────────────────────────────────┘
```

## 🎯 Component Interaction Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        🔄 COMPONENT INTERACTION FLOW                           │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │    👤 User  │    │   🏠 Group  │    │  💰 Expense │    │💸 Transaction│
    │             │    │             │    │             │    │             │
    │ • Observer  │◄──►│ • Subject   │◄──►│ • Subject   │◄──►│ • Subject   │
    │ • Balance   │    │ • Members   │    │ • Splits    │    │ • Status    │
    │ • Groups    │    │ • Expenses │    │ • Strategy  │    │ • Amount    │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
           │                   │                   │                   │
           │                   │                   │                   │
           ▼                   ▼                   ▼                   ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │📊 BalanceSheet│   │🧮 Simplify │   │⚙️ SplitStrategy│   │📋 Status    │
    │             │    │            │    │             │    │             │
    │ • Thread-safe│    │ • Heap algo│    │ • Equal     │    │ • PENDING   │
    │ • Lock-based│    │ • Minimize │    │ • Percent   │    │ • COMPLETED │
    │ • Real-time │    │ • Optimal  │    │ • Exact     │    │ • FAILED    │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 🎨 Design Pattern Visualization

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        🎭 DESIGN PATTERNS IN ACTION                            │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  🔒 SINGLETON PATTERN                                                          │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                    SplitWiseService                                    │    │
│  │                                                                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │    │
│  │  │   Instance  │  │    Lock     │  │  Services   │                    │    │
│  │  │  (Single)   │  │ (Thread-safe)│  │ (Facade)   │                    │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                    │    │
│  │                                                                         │    │
│  │  🎯 Ensures only ONE instance across the entire application            │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  🏛️ FACADE PATTERN                                                             │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                    SplitWiseService                                    │    │
│  │                                                                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │    │
│  │  │ UserService │  │GroupService │  │   Complex   │                    │    │
│  │  │             │  │             │  │ Operations  │                    │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                    │    │
│  │                                                                         │    │
│  │  🎯 Provides SIMPLE interface to COMPLEX subsystems                     │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  ⚙️ STRATEGY PATTERN                                                           │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                    SplitStrategy (Abstract)                            │    │
│  │                                                                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │    │
│  │  │    Equal    │  │   Percent   │  │    Exact    │                    │    │
│  │  │   Strategy  │  │  Strategy   │  │  Strategy   │                    │    │
│  │  │             │  │             │  │             │                    │    │
│  │  │ Split ₹1000 │  │ Split ₹1000 │  │ Split ₹1000 │                    │    │
│  │  │ equally     │  │ by %        │  │ by amounts  │                    │    │
│  │  │ ₹333 each   │  │ 40%,30%,30% │  │ ₹500,₹300  │                    │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                    │    │
│  │                                                                         │    │
│  │  🎯 Different ALGORITHMS for expense splitting                         │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  👁️ OBSERVER PATTERN                                                           │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                    Subject (Abstract)                                 │    │
│  │                                                                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │    │
│  │  │   Group     │  │  Expense    │  │ Transaction │                    │    │
│  │  │  Subject    │  │  Subject    │  │  Subject    │                    │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                    │    │
│  │         │                 │                 │                         │    │
│  │         ▼                 ▼                 ▼                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │    │
│  │  │   User      │  │   User      │  │   User      │                    │    │
│  │  │ (Observer)  │  │ (Observer)  │  │ (Observer)  │                    │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                    │    │
│  │                                                                         │    │
│  │  🎯 REAL-TIME notifications for all events                             │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  🔨 BUILDER PATTERN                                                             │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                    ExpenseBuilder                                       │    │
│  │                                                                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │    │
│  │  │set_description│ │set_amount()│ │set_paid_by()│                    │    │
│  │  │()            │  │            │  │            │                    │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                    │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │    │
│  │  │set_participants│ │set_strategy│ │   build()   │                    │    │
│  │  │()            │  │()          │  │            │                    │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                    │    │
│  │                                                                         │    │
│  │  🎯 COMPLEX object construction with VALIDATION                        │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Key Features Visualization

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        🌟 ADVANCED FEATURES HIGHLIGHTED                       │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  🧮 DEBT SIMPLIFICATION ALGORITHM                                              │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                    Group.simplify_expenses()                           │    │
│  │                                                                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │    │
│  │  │   Step 1    │  │   Step 2    │  │   Step 3    │                    │    │
│  │  │ Calculate   │  │ Create      │  │ Generate    │                    │    │
│  │  │ Net Balances│  │ Min-Heaps   │  │ Transactions│                    │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                    │    │
│  │                                                                         │    │
│  │  📊 Before: 6 expenses → 12+ individual payments                      │    │
│  │  📊 After:  6 expenses → 3 optimal transactions                       │    │
│  │                                                                         │    │
│  │  🎯 Minimizes total number of transactions needed                       │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  🔒 THREAD SAFETY                                                              │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                    BalanceSheet                                        │    │
│  │                                                                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │    │
│  │  │    Lock     │  │adjust_balance│  │Concurrent   │                    │    │
│  │  │(Thread-safe)│  │()           │  │Operations   │                    │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                    │    │
│  │                                                                         │    │
│  │  🎯 Multiple users can update balances simultaneously                  │    │
│  │  🎯 Data consistency maintained with locks                            │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  📢 REAL-TIME NOTIFICATIONS                                                   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                    Observer Pattern                                    │    │
│  │                                                                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │    │
│  │  │expense_update│ │transaction_update│ │update_group│                    │    │
│  │  │()           │  │()            │  │()          │                    │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                    │    │
│  │                                                                         │    │
│  │  🎯 Instant notifications for all events                               │    │
│  │  🎯 Method-specific handling for different event types                │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📋 Summary Table

| Component           | Pattern            | Key Feature                       | Purpose                      |
| ------------------- | ------------------ | --------------------------------- | ---------------------------- |
| 🏢 SplitWiseService | Singleton + Facade | Single instance, Simple interface | Central service coordination |
| 👤 User             | Observer           | Real-time notifications           | Event handling               |
| 🏠 Group            | Subject            | Member management                 | Group operations             |
| 💰 Expense          | Subject            | Split calculations                | Expense handling             |
| 💸 Transaction      | Subject            | Status tracking                   | Payment processing           |
| 📊 BalanceSheet     | Thread-safe        | Concurrent updates                | Balance management           |
| ⚙️ SplitStrategy    | Strategy           | Multiple algorithms               | Flexible splitting           |
| 🔨 ExpenseBuilder   | Builder            | Complex construction              | Object creation              |
| 👁️ Observer         | Observer           | Event notifications               | Real-time updates            |

This pictorial representation provides an easy-to-understand visual overview of your Splitwise architecture! 🎉✨
