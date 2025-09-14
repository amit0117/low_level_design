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
