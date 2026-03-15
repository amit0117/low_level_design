"""
Mermaid Diagrams for Online Shopping Service - Low Level Design
"""

DATA_FLOW_DIAGRAM = """
```mermaid
graph TD
    User[User] -->|has| Account[Account]
    Account -->|has| Address[Address]

    User -->|searches via| SearchStrategy{Search Strategy}
    SearchStrategy -->|by name| NameSearch[SearchByNameStrategy]
    SearchStrategy -->|by category| CategorySearch[SearchByCategoryStrategy]
    SearchStrategy -->|by price| PriceSearch[SearchByPriceRangeStrategy]

    User -->|adds to| ShoppingCart[ShoppingCart]
    ShoppingCart -->|contains| CartItem[CartItem]
    CartItem -->|references| Product[Product]

    Product -->|decorated by| ProductDecorator{Product Decorator}
    ProductDecorator -->|gift wrap| GiftWrapper[GiftWrapperDecorator]

    ShoppingCart -->|checkout creates| Order[Order]
    Order -->|contains| OrderItem[OrderItem]
    Order -->|has| OrderState{Order State}
    OrderState -->|pending| PendingState[PendingState]
    OrderState -->|cancelled| CancelledState[CancelledState]
    OrderState -->|delivered| DeliveredState[DeliveredState]

    Order -->|paid via| PaymentService[PaymentService]
    PaymentService -->|uses| PaymentStrategy{Payment Strategy}
    PaymentStrategy -->|credit card| CreditCard[CreditCardPaymentStrategy]
    PaymentStrategy -->|debit card| DebitCard[DebitCardPaymentStrategy]
    PaymentStrategy -->|COD| COD[CashOnDeliveryPaymentStrategy]
    PaymentStrategy -->|UPI| UPI[UpiPaymentStrategy]

    Product -->|tracked by| InventoryService[InventoryService Subject]
    InventoryService -->|notifies| InStockObserver[InStockToOutOfStockObserver]
    InventoryService -->|notifies| OutOfStockObserver[OutOfStockToInStockObserver]

    Order -->|observed by| CustomerObserver[CustomerOrderObserver]
    Order -->|observed by| AdminObserver[AdminOrderObserver]
```
"""

USER_FLOW_DIAGRAM = """
```mermaid
sequenceDiagram
    actor User
    participant Search as SearchStrategy
    participant Cart as ShoppingCart
    participant Inventory as InventoryService
    participant Decorator as ProductDecorator
    participant Order
    participant Payment as PaymentService
    participant Observer as OrderObserver

    User->>Search: Search products (name/category/price)
    Search-->>User: Matching products

    User->>Cart: Add product to cart
    Cart->>Inventory: Check stock availability
    Inventory-->>Cart: In stock confirmed
    Cart-->>User: Item added

    User->>Decorator: Add gift wrap to product
    Decorator-->>Cart: Decorated product in cart

    User->>Cart: Proceed to checkout
    Cart->>Order: Create order from cart items
    Note over Order: State = PendingState

    User->>Payment: Select payment method
    alt Credit Card
        Payment->>Payment: Process credit card
    else UPI
        Payment->>Payment: Process UPI
    else Cash on Delivery
        Payment->>Payment: Mark COD
    end

    alt Payment successful
        Payment-->>Order: Payment confirmed
        Order->>Inventory: Deduct stock
        Inventory->>Inventory: Update quantities

        alt Stock depleted
            Inventory->>Observer: Notify out of stock
        end

        Order->>Observer: Notify customer (order confirmed)
        Order->>Observer: Notify admin (new order)
        Observer-->>User: Order confirmation

        Note over Order: Shipping & Delivery...
        Note over Order: State = DeliveredState
        Order->>Observer: Notify delivered
    else Payment failed
        Payment-->>User: Payment failed
        Note over Order: State = CancelledState
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
