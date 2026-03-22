# Online Stock Exchange

## Data Flow Diagram

```mermaid
graph TD
    User[User] -->|owns| Account[Account]
    Account -->|holds| Cash[Cash Balance]
    Account -->|holds| Stocks[Stock Holdings]

    User -->|creates via| OrderBuilder[OrderBuilder]
    OrderBuilder -->|builds| Order[Order]
    Order -->|has| OrderState{Order State}
    OrderState -->|created| CreatedState[CreatedState]
    OrderState -->|open| OpenState[OpenState]
    OrderState -->|partial| PartiallyFilledState[PartiallyFilledState]
    OrderState -->|filled| FilledState[FilledState]
    OrderState -->|cancelled| CancelledState[CancelledState]
    OrderState -->|rejected| RejectedState[RejectedState]
    OrderState -->|expired| ExpiredState[ExpiredState]

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

## Order lifecycle (states)

| State | Meaning |
|-------|---------|
| **Created** | Order object built; not yet accepted by the exchange. |
| **Open (Active)** | Live in the order book; waiting to match with a counter order. |
| **Partially Filled** | Some quantity executed; remainder still open (e.g. buy 100 → 40 filled, 60 pending). |
| **Filled (Executed)** | Entire quantity matched and completed. |
| **Cancelled** | User or system cancels before full execution. |
| **Rejected** | Never reaches execution: invalid price/quantity, insufficient funds, or exchange rule violation. |
| **Expired** | Validity ended (e.g. session or order validity window closed). |

**Typical flow**

`Created → Open → (Partially Filled)* → Filled` **or** `Cancelled` **or** `Expired` **or** `Rejected`

*(Early validation failures can go `Created → Rejected` without ever being **Open**.)*

## User Flow Diagram

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
    Note over Order: State = CreatedState

    User->>StockExchange: Submit order (Buy/Sell)
    alt Validation fails
        StockExchange-->>User: Reject (invalid price/qty, insufficient funds, rule violation)
        Note over Order: State = RejectedState
    else Accepted into order book
        StockExchange->>Order: Accept
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
        else No Match / remainder handling
            Note over Order: Unfilled portion may stay Open or be closed per exchange rules
        else Order validity ended
            Note over Order: State = ExpiredState
        end
        User->>StockExchange: Cancel remaining order (optional)
        StockExchange->>Order: CancelOrderCommand
        Note over Order: State = CancelledState (if still Open / Partially Filled)
    end

    Stock->>User: Notify price change
    Note over User: Receives real-time updates
```
