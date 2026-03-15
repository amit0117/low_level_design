"""
Mermaid Diagrams for Online Auction System - Low Level Design
"""

DATA_FLOW_DIAGRAM = """
```mermaid
graph TD
    Seller[Seller/User] -->|creates| Auction[Auction]
    Auction -->|contains| AuctionItem[AuctionItem]
    Auction -->|has| AuctionState{Auction State}
    AuctionState -->|active| ActiveState[ActiveAuctionState]
    AuctionState -->|closed| ClosedState[ClosedAuctionState]

    Auction -->|stored in| AuctionRepository[AuctionRepository]
    Auction -->|managed by| OnlineAuctionSystem[OnlineAuctionSystem]

    Buyer[Buyer/User] -->|places| Bid[Bid]
    Bid -->|validated by| AuctionValidator{Auction Validator}
    AuctionValidator -->|decorated| ValidatorDecorator[AuctionValidatorDecorator]

    Bid -->|processed by| AuctionHandler{Auction Handler Chain}
    AuctionHandler -->|base| BaseHandler[BaseAuctionHandler]

    Auction -->|mediated by| AuctionMediator[AuctionMediator]
    AuctionMediator -->|coordinates| Seller
    AuctionMediator -->|coordinates| Buyer

    Buyer -->|searches via| SearchStrategy{Auction Search Strategy}
    SearchStrategy -->|by title| TitleSearch[AuctionItemTitleSearchStrategy]
    SearchStrategy -->|by price| PriceSearch[AuctionItemStartingPriceRangeSearchStrategy]
    SearchStrategy -->|by status| StatusSearch[AuctionStatusSearchStrategy]

    Auction -->|notifies| AuctionObserver[AuctionObserver]
    AuctionObserver -->|updates| Buyer
    AuctionObserver -->|updates| Seller
```
"""

USER_FLOW_DIAGRAM = """
```mermaid
sequenceDiagram
    actor Seller
    actor Buyer
    participant AuctionSystem as OnlineAuctionSystem
    participant Auction
    participant Validator as AuctionValidator
    participant Handler as AuctionHandler
    participant Mediator as AuctionMediator
    participant Observer as AuctionObserver

    Seller->>AuctionSystem: Create auction with item & starting price
    AuctionSystem->>Auction: Initialize auction
    Note over Auction: State = ActiveAuctionState

    Buyer->>AuctionSystem: Search auctions (by title/price/status)
    AuctionSystem-->>Buyer: Matching auctions

    Buyer->>Auction: Place bid (amount)
    Auction->>Validator: Validate bid
    Validator->>Validator: Check bid > current price
    Validator->>Validator: Check auction is active
    Validator->>Validator: Check user is valid

    alt Valid bid
        Validator-->>Auction: Bid accepted
        Auction->>Handler: Process bid through chain
        Handler-->>Auction: Bid recorded
        Auction->>Observer: Notify bid placed
        Observer-->>Seller: New bid notification
        Observer-->>Buyer: Bid confirmation
    else Invalid bid
        Validator-->>Buyer: Bid rejected (reason)
    end

    Note over Buyer: More buyers place bids...

    Seller->>AuctionSystem: End auction
    AuctionSystem->>Auction: Close auction
    Note over Auction: State = ClosedAuctionState

    Auction->>Mediator: Determine winner
    Mediator->>Mediator: Highest bidder wins
    Mediator->>Observer: Notify auction result
    Observer-->>Seller: Winner details
    Observer-->>Buyer: Won/Lost notification

    Mediator->>Mediator: Process payment
    Mediator->>Mediator: Transfer item to winner
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
