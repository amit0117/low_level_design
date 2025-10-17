from enum import Enum


class AuctionItemType(Enum):
    PHYSICAL = "physical"
    DIGITAL = "digital"
    SERVICE = "service"


class AuctionStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    CLOSED = "closed"
    SETTLED = "settled"
    CANCELLED = "cancelled"


class AuctionType(Enum):
    ENGLISH = "english"  # Start with the starting price and incrementally increase the price and the highest bidder wins and pay their own bid amount
    DUTCH = "dutch"  # Start with the starting price and incrementally decrease the price and the first bidder to accept the price wins and pay their own bid amount
    SEALED_BID = "sealed_bid"  # Bidders submit bids in secret and the highest bidder wins and pay their own bid amount
    SECOND_PRICE_AUCTION = "second_price_auction"  # Bidders submit bids in secret , The highest bidder wins and but pay the second highest bid amount
    REVERSE_AUCTION = "reverse_auction"  # Buyers posts a request for a product and the sellers competes to provide the best lowest price, The Lowest price wins and the buyer pays the lowest price and buyer pay the minimum price to the seller


class PaymentStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILURE = "failure"


class PaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    CASH = "cash"
