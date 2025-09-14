from abc import ABC, abstractmethod
from app.models.order import Order
from app.models.enums import OrderType, OrderStatus
from app.models.account import Account
from app.models.stock_exchange import StockExchange
from app.exceptions import InsufficientFundException, InsufficientStockException


class OrderCommand(ABC):
    @abstractmethod
    def execute(self):
        pass


class BuyStockCommand(OrderCommand):
    def __init__(self, account: Account, order: Order):
        self.account = account
        self.order = order
        self.stock_exchange = StockExchange.get_instance()

    def execute(self):
        # Validate based on order type
        self._validate_buy_order()

        print(f"Placing BUY order for {self.order}")
        self.stock_exchange.place_buy_order(self.order)
        # add this order to the owner's orders
        self.order.get_owner().add_order(self.order)

    def _validate_buy_order(self):
        """Validate buy order based on order type"""
        order_type = self.order.get_type()

        if order_type == OrderType.MARKET:
            self._validate_market_buy()
        elif order_type == OrderType.LIMIT:
            self._validate_limit_buy()
        elif order_type == OrderType.STOP_LOSS:
            self._validate_stop_loss_buy()
        elif order_type == OrderType.STOP_LIMIT:
            self._validate_stop_limit_buy()

    def _validate_market_buy(self):
        """Market order: Can't validate exact funds. Will be validated when executed."""
        return

    def _validate_limit_buy(self):
        """Limit order: Can validate exact funds needed"""
        required_funds = self.order.get_quantity() * self.order.get_limit_price()

        if self.account.get_balance() < required_funds:
            raise InsufficientFundException(
                f"Insufficient funds for limit buy order. Required: ${required_funds:.2f}, Available: ${self.account.get_balance():.2f}"
            )

        print(f"Limit buy order validated - required funds: ${required_funds:.2f}")

    def _validate_stop_loss_buy(self):
        """Stop loss buy: Validate stop price and rough fund estimate"""
        # Order should have at least some stop price
        stop_price = self.order.get_stop_price()
        current_price = self.order.get_stock().get_price()
        if self.account.get_balance() < self.order.get_quantity() * min(stop_price, current_price):
            raise InsufficientFundException(
                f"Insufficient funds for stop loss buy order. Required: ${self.order.get_quantity() *min(stop_price, current_price):.2f}, Available: ${self.account.get_balance():.2f}"
            )

        print(f"Stop loss buy order - stop price: ${stop_price:.2f}, current price: ${current_price:.2f}")

    def _validate_stop_limit_buy(self):
        """Stop limit buy: Validate stop price, limit price, and exact funds"""
        # Order should have at least some stop price and after that it will behave as limit order
        stop_price = self.order.get_stop_price()
        current_price = self.order.get_stock().get_price()
        if self.account.get_balance() < self.order.get_quantity() * min(stop_price, current_price):
            raise InsufficientFundException(
                f"Insufficient funds for stop limit buy order. Required: ${self.order.get_quantity() *min(stop_price, current_price):.2f}, Available: ${self.account.get_balance():.2f}"
            )
        # also verify that it should respect the limit price
        if self.order.get_limit_price() < self.order.get_stock().get_price():
            print(f"Limit price (${self.order.get_limit_price():.2f}) should not be below current price (${self.order.get_stock().get_price():.2f})")
            raise Exception("Limit price should not be below current price")
        print(f"Stop limit buy order - stop price: ${stop_price:.2f}, current price: ${current_price:.2f}")


class SellStockCommand(OrderCommand):
    def __init__(self, account: Account, order: Order):
        self.account = account
        self.order = order
        self.stock_exchange = StockExchange.get_instance()

    def execute(self):
        # validate that the quantity available is greater than the quantity to sell
        if self.account.get_stock_quantity(self.order.get_stock().get_symbol()) < self.order.get_quantity():
            raise InsufficientStockException(
                f"Insufficient shares for sell order. Required: {self.order.get_quantity()}, Available: {self.account.get_stock_quantity(self.order.get_stock().get_symbol())}"
            )

        print(f"Placing SELL order for {self.order}")
        self.stock_exchange.place_sell_order(self.order)
        # add this order to the owner's orders
        self.order.get_owner().add_order(self.order)


# Additional command for order cancellation
class CancelOrderCommand(OrderCommand):
    def __init__(self, order: Order):
        self.order = order

    def execute(self):
        if self.order.get_status() not in [OrderStatus.OPEN, OrderStatus.PARTIALLY_FILLED]:
            raise Exception(f"Cannot cancel order in {self.order.get_status().value} status")

        print(f"Cancelling order {self.order.order_id} with status {self.order.get_status().value}")
        self.order.cancel()
        # remove this order from the owner's orders
        self.order.get_owner().remove_order(self.order)
