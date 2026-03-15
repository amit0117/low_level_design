"""
Mermaid Diagrams for Restaurant Management Service - Low Level Design
"""

DATA_FLOW_DIAGRAM = """
```mermaid
graph TD
    Customer[Customer] -->|reserves| Table[Table]
    Table -->|has| TableState{Table State}
    TableState -->|available| AvailableState[AvailableTableState]
    TableState -->|occupied| OccupiedState[OccupiedTableState]

    Staff[Staff] -->|roles| StaffRoles{Staff Roles}
    StaffRoles -->|manager| Manager[Manager]
    StaffRoles -->|chef| Chef[Chef]
    StaffRoles -->|waiter| Waiter[Waiter]

    Waiter -->|takes| Order[Order Subject]
    Order -->|contains| OrderItem[OrderItem]
    OrderItem -->|has| OrderItemState[OrderItemState]
    OrderItem -->|references| MenuItem[Menu Item]

    Menu[Menu] -->|stored in| MenuRepository[MenuRepository]
    Menu -->|categorized by| MenuCategory[MenuCategory]
    MenuItem -->|type| ItemType{Item Type}
    ItemType -->|veg| VegItem[VegItem]
    ItemType -->|non-veg| NonVegItem[NonVegItem]

    Chef -->|prepares| OrderItem
    Order -->|observed by| OrderObserver[OrderObserver]

    Inventory[Inventory] -->|managed by| InventoryService[InventoryService]
    InventoryService -->|stored in| InventoryRepository[InventoryRepository]
    Inventory -->|observed by| InventoryObserver[InventoryObserver]
    InventoryObserver -->|alerts| Manager

    Table -->|observed by| TableObserver[TableObserver]

    Order -->|generates| Bill[Bill]
    Bill -->|decorated by| BillDecorator{Bill Decorator}
    BillDecorator -->|discount| DiscountDecorator[DiscountDecorator]

    Bill -->|paid via| PaymentStrategy{Payment Strategy}
    PaymentStrategy -->|cash| CashPayment[CashPayment]
    PaymentStrategy -->|card| CardPayment[CardPayment]
    PaymentStrategy -->|credit card| CreditCard[CreditCardPayment]
    PaymentStrategy -->|UPI| UpiPayment[UpiPayment]
```
"""

USER_FLOW_DIAGRAM = """
```mermaid
sequenceDiagram
    actor Customer
    actor Waiter
    actor Chef
    actor Manager
    participant Table
    participant Menu
    participant Order
    participant Inventory as InventoryService
    participant BillDecorator
    participant Payment as PaymentStrategy

    Customer->>Table: Request table
    Note over Table: State = OccupiedTableState

    Waiter->>Menu: Show menu to customer
    Menu-->>Customer: Available items (veg/non-veg)

    Customer->>Waiter: Place order
    Waiter->>Order: Create order with items
    Order->>Inventory: Check ingredient availability
    Inventory-->>Order: Ingredients available

    Order->>Chef: Send to kitchen
    Note over Chef: Preparing food

    Chef->>Order: Mark item as prepared
    Order->>Waiter: Notify dish ready
    Waiter->>Customer: Serve dish

    Note over Customer: Enjoying meal...

    Customer->>Waiter: Request bill
    Waiter->>Order: Generate bill
    Order->>BillDecorator: Calculate total
    BillDecorator->>BillDecorator: Apply base price
    BillDecorator->>BillDecorator: Apply discount (if any)
    BillDecorator-->>Waiter: Final bill amount

    Waiter-->>Customer: Present bill
    Customer->>Payment: Pay bill
    alt Cash
        Payment-->>Waiter: Cash payment received
    else Card / Credit Card
        Payment-->>Waiter: Card payment processed
    else UPI
        Payment-->>Waiter: UPI payment confirmed
    end

    Waiter->>Table: Release table
    Note over Table: State = AvailableTableState

    Inventory->>Manager: Alert if stock low
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
