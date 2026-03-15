"""
Mermaid Diagrams for Online Stock Exchange - Low Level Design
"""

DATA_FLOW_DIAGRAM = """
```mermaid
graph TD
    User[User] -->|owns| Account[Account]
    Account -->|holds| Cash[Cash Balance]
    Account -->|holds| Stocks[Stock Holdings]

    User -->|creates via| OrderBuilder[OrderBuilder]
    OrderBuilder -->|builds| Order[Order]
    Order -->|has| OrderState{Order State}
    OrderState -->|open| OpenState[OpenState]
    OrderState -->|filled| FilledState[FilledState]
    OrderState -->|partial| PartiallyFilledState[PartiallyFilledState]
    OrderState -->|cancelled| CancelledState[CancelledState]
    OrderState -->|failed| FailedState[FailedState]

    Order -->|uses| ExecutionStrategy{Execution Strategy}
    ExecutionStrategy -->|market| MarketOrder[MarketOrder]
    ExecutionStrategy -->|limit| LimitOrder[LimitOrder]
    ExecutionStrategy -->|stop loss| StopLossOrder[StopLossOrder]
    ExecutionStrategy -->|stop limit| StopLimitOrder[StopLimitOrder]

    Order -->|executed via| OrderCommand{Order Command}
    OrderCommand -->|buy| BuyStockCommand[BuyStockCommand]
    OrderCommand -->|sell| SellStockCommand[SellStockCommand]
    OrderCommand -->|cancel| CancelOrderCommand[CancelOrderCommand]

    OrderCommand -->|submitted to| StockExchange[StockExchange]
    StockExchange -->|matches orders| StockBrokerageSystem[StockBrokerageSystem]
    StockBrokerageSystem -->|updates| Account

    Stock[Stock Subject] -->|price changes| StockObserver[StockObserver]
    StockObserver -->|notifies| User
    StockExchange -->|manages| Stock
```
"""

USER_FLOW_DIAGRAM = """
```mermaid
sequenceDiagram
    actor User
    participant Account
    participant OrderBuilder
    participant Order
    participant StockExchange
    participant BrokerageSystem as StockBrokerageSystem
    participant Stock

    User->>Account: Register with initial cash/stocks
    Account-->>User: Account created

    User->>Stock: Subscribe to price updates
    Note over Stock: Observer pattern

    User->>OrderBuilder: Configure order parameters
    OrderBuilder->>OrderBuilder: Set stock, quantity, strategy
    OrderBuilder->>Order: Build order
    Note over Order: State = OpenState

    alt Buy Order
        User->>StockExchange: Place BuyStockCommand
        StockExchange->>BrokerageSystem: Match with sell orders
    else Sell Order
        User->>StockExchange: Place SellStockCommand
        StockExchange->>BrokerageSystem: Match with buy orders
    end

    alt Order Matched Fully
        BrokerageSystem->>Account: Update cash & stock balances
        Note over Order: State = FilledState
    else Order Partially Matched
        BrokerageSystem->>Account: Partial update
        Note over Order: State = PartiallyFilledState
    else No Match Found
        Note over Order: State = FailedState
    end

    User->>StockExchange: Cancel remaining order
    StockExchange->>Order: CancelOrderCommand
    Note over Order: State = CancelledState

    Stock->>User: Notify price change
    Note over User: Receives real-time updates
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
