# Online Stock Exchange System

A comprehensive stock exchange system implementing various design patterns and order types.

## Features

### Order Types Supported

- **Market Orders**: Execute immediately at current market price
- **Limit Orders**: Execute only at specified price or better
- **Stop Loss Orders**: Trigger when price reaches stop price, then execute as market order
- **Stop Limit Orders**: Trigger when price reaches stop price, then execute as limit order

### Design Patterns Implemented

- **Singleton Pattern**: StockBrokerageSystem and StockExchange
- **Command Pattern**: Order execution with validation
- **Observer Pattern**: Stock price change notifications
- **State Pattern**: Order state management
- **Strategy Pattern**: Execution strategies for different order types

## Running the Demo

### Prerequisites

- Python 3.7+
- All required dependencies installed

### Quick Start

```bash
cd low_level_design/OnlineStockExchange
python run.py
```

### What the Demo Shows

1. **System Setup**: Creates users with initial balances and stocks
2. **Market Orders**: Demonstrates immediate execution at market price
3. **Limit Orders**: Shows price-based order matching
4. **Stop Loss Orders**: Demonstrates price-triggered execution
5. **Stop Limit Orders**: Shows complex price-triggered limit execution
6. **Order Cancellation**: Tests order cancellation scenarios
7. **Error Handling**: Demonstrates insufficient funds/stock handling

### Demo Scenarios

#### Initial Setup

- **Alice**: $50,000 cash
- **Bob**: $75,000 cash + 100 AAPL shares
- **Charlie**: $100,000 cash + 20 GOOGL + 50 TSLA shares

#### Stock Prices

- **AAPL**: $150.00
- **GOOGL**: $2,800.00
- **TSLA**: $200.00

#### Order Examples

- Market buy/sell orders
- Limit orders with price matching
- Stop loss orders triggered by price changes
- Stop limit orders with complex price logic
- Order cancellation attempts
- Error handling for insufficient funds/stocks

## 📊 Entity Relationship Diagram

### Core Entities and Relationships

```
┌─────────────────────────────────────┐
│   StockBrokerageSystem              │
│─────────────────────────────────────│
│ (Singleton)                         │
│ - users (Dict<User>)                │
│ - stocks (Dict<Stock>)              │
└──────┬──────────────────────────────┘
       │
       │ 1..* (manages)
       │
       ▼
┌─────────────────────────────────────┐
│            User                     │
│─────────────────────────────────────│
│ user_id                             │
│ name                                │
│ account (Account)                   │
│ orders (List<Order>)                │
└──────┬──────────────────────────────┘
       │
       │ 1 (has)
       │
       ▼
┌─────────────────────────────────────┐
│          Account                    │
│─────────────────────────────────────│
│ balance                             │
│ portfolio (Dict<Stock, Int>)        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│            Stock                    │
│─────────────────────────────────────│
│ symbol                              │
│ price                               │
│ observers (List<Observer>)          │
└──────┬──────────────────────────────┘
       │
       │ 1..* (traded in)
       │
       ▼
┌─────────────────────────────────────┐
│            Order                    │
│─────────────────────────────────────│
│ order_id                            │
│ owner (User)                        │
│ stock (Stock)                       │
│ order_type (OrderType)              │
│ quantity                            │
│ price (Optional)                    │
│ stop_price (Optional)               │
│ status (OrderStatus)                │
│ state (OrderState)                  │
│ execution_strategy                  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│       StockExchange                 │
│─────────────────────────────────────│
│ (Singleton)                         │
│ - buy_orders (Dict)                 │
│ - sell_orders (Dict)                │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│      ExecutionStrategy              │
│─────────────────────────────────────│
│ (Abstract)                          │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┬──────────────┬──────────────┬
       ▼              ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Market    │ │   Limit     │ │  StopLoss   │ │ StopLimit   │
│  Strategy   │ │  Strategy   │ │  Strategy   │ │  Strategy   │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘

┌─────────────────────────────────────┐
│        OrderState                   │
│─────────────────────────────────────│
│ (Abstract)                          │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┬──────────────┬
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Pending    │ │  Executed   │ │  Cancelled  │
│   State     │ │   State     │ │   State     │
└─────────────┘ └─────────────┘ └─────────────┘
```

### Entity Relationships

1. **StockBrokerageSystem ↔ User** (One-to-Many)

   - System manages multiple Users
   - Users stored in dictionary

2. **StockBrokerageSystem ↔ Stock** (One-to-Many)

   - System manages multiple Stocks
   - Stocks stored in dictionary

3. **User ↔ Account** (One-to-One)

   - Each User has one Account
   - Account tracks balance and portfolio

4. **User ↔ Order** (One-to-Many)

   - A User can place multiple Orders
   - Each Order belongs to one User (owner)

5. **Order ↔ Stock** (Many-to-One)

   - An Order is for one Stock
   - A Stock can have multiple Orders

6. **Order ↔ ExecutionStrategy** (One-to-One)

   - Each Order uses one ExecutionStrategy
   - Strategy determines execution logic

7. **Order ↔ OrderState** (One-to-One)

   - Each Order has one current State
   - State transitions: Pending → Executed/Cancelled

8. **Stock ↔ User (Observer Pattern)**

   - Stock implements `StockSubject`
   - User implements `StockObserver`
   - Users notified on price changes

9. **StockExchange ↔ Order** (One-to-Many)

   - StockExchange manages buy_orders and sell_orders
   - Orders matched and executed by exchange

10. **Command Pattern Relationships**
    - BuyStockCommand, SellStockCommand, CancelOrderCommand
    - Commands encapsulate order operations

## 🔄 Data Flow Diagrams

### 1. Order Placement Flow

```
┌──────────┐
│   User   │
└────┬─────┘
     │
     │ 1. place_order()
     ▼
┌─────────────────┐
│StockBrokerageSys│
└────┬────────────┘
     │
     │ 2. Create OrderCommand
     ▼
┌─────────────────┐
│ OrderCommand    │
│  (Command)      │
└────┬────────────┘
     │
     │ 3. execute()
     │ 4. Validate order
     ▼
┌─────────────────┐
│ StockExchange   │
└────┬────────────┘
     │
     │ 5. Add to order book
     │ 6. Try to match orders
     ▼
┌─────────────────┐
│  Order Matching │
└────┬────────────┘
     │
     │ 7. Execute if matched
     │ 8. Update account
     │ 9. notify_observers()
     ▼
┌─────────────────┐
│   Observers     │
│  (Notified)     │
└─────────────────┘
```

### 2. Stock Price Update Flow

```
┌──────────┐
│  System  │
└────┬─────┘
     │
     │ 1. update_price()
     ▼
┌─────────────────┐
│     Stock       │
└────┬────────────┘
     │
     │ 2. Update price
     │ 3. Check stop orders
     │ 4. notify_observers()
     ▼
┌─────────────────┐
│  All Observers  │
│  (Users)        │
└────┬────────────┘
     │
     │ 5. Trigger stop orders
     ▼
┌─────────────────┐
│  Stop Orders    │
│  (Executed)     │
└─────────────────┘
```

### 3. Complete System Interaction Flow

```
┌──────────────┐
│   Client     │
│  (run.py)    │
└──────┬───────┘
       │
       │ All Operations
       ▼
┌─────────────────────────────────────┐
│   StockBrokerageSystem              │
│   (Singleton)                       │
│  - User Management                  │
│  - Stock Management                 │
│  - Order Processing                 │
└──────┬──────────────────────────────┘
       │
       ├──────────────────┬──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐  ┌─────────────┐  ┌──────────────┐
│    Users    │  │   Stocks    │  │ StockExchange│
│  - Accounts │  │             │  │              │
│  - Orders   │  │             │  │              │
└─────────────┘  └─────────────┘  └──────────────┘
       │                  │                  │
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Orders     │  │ Execution   │  │ OrderState  │
│             │  │ Strategies  │  │  (State     │
│             │  │             │  │   Pattern)  │
└─────────────┘  └─────────────┘  └─────────────┘
```

## 📋 Entity Attributes Summary

### User Entity

- `user_id`: Unique identifier (UUID)
- `name`: User's name
- `account`: Account object
- `orders`: List of Order objects

### Account Entity

- `balance`: Cash balance
- `portfolio`: Dictionary mapping stock symbol to quantity

### Stock Entity

- `symbol`: Stock symbol (e.g., "AAPL")
- `price`: Current stock price
- `observers`: List of Observer objects

### Order Entity

- `order_id`: Unique identifier (UUID)
- `owner`: User who placed the order
- `stock`: Stock being traded
- `order_type`: OrderType (BUY, SELL)
- `quantity`: Number of shares
- `price`: Limit price (for limit orders)
- `stop_price`: Stop price (for stop orders)
- `status`: OrderStatus (PENDING, EXECUTED, CANCELLED)
- `state`: OrderState object
- `execution_strategy`: ExecutionStrategy object

## System Architecture

```
Client Request
     ↓
StockBrokerageSystem (Invoker)
     ↓
OrderCommand (Command)
     ↓
StockExchange (Receiver)
     ↓
Order Execution & Matching
```

## Key Components

- **StockBrokerageSystem**: Main system orchestrator
- **StockExchange**: Order matching and execution engine
- **Order Commands**: Validation and execution logic
- **Execution Strategies**: Order type-specific behavior
- **Order States**: State management for orders
- **Observer Pattern**: Real-time price notifications

## Error Handling

The system handles various error scenarios:

- Insufficient funds for buy orders
- Insufficient stock for sell orders
- Invalid order parameters
- Order cancellation restrictions

## Extensibility

The system is designed to be easily extensible:

- Add new order types by implementing ExecutionStrategy
- Add new validation rules in OrderCommand classes
- Extend notification system with Observer pattern
- Add new order states as needed
