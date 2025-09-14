"""
Online Stock Exchange System Demo
Demonstrates all order types: Market, Limit, Stop Loss, and Stop Limit orders
"""

import time
from app.models.stock_brokerage_system import StockBrokerageSystem
from app.models.user import User
from app.models.stock import Stock
from app.models.order import OrderBuilder


def print_separator(title: str):
    """Print a formatted separator with title"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_account_status(user: User) -> None:
    """Print user account status"""
    print(f"👤 {user.get_name()}")
    print(f"   💰 Cash: ${user.get_account().get_balance():.2f}")
    print(f"   📈 Portfolio: {user.get_account().get_portfolio()}")
    print(f"   📋 Orders: {len(user.get_orders())}")


def print_stock_status(stock: Stock) -> None:
    """Print stock current status"""
    print(f"📊 {stock.get_symbol()}: ${stock.get_price():.2f}")


def print_order_details(order, title: str = "Order Details"):
    """Print order details"""
    print(f"\n📋 {title}:")
    print(f"   ID: {order.order_id}")
    print(f"   Type: {order.order_type.value}")
    print(f"   Transaction: {order.transaction_type.value}")
    print(f"   Quantity: {order.get_quantity()}")
    print(f"   Status: {order.get_status().value}")
    if order.get_limit_price():
        print(f"   Limit Price: ${order.get_limit_price():.2f}")
    if order.get_stop_price():
        print(f"   Stop Price: ${order.get_stop_price():.2f}")
    print(f"   Triggered: {getattr(order, 'has_triggered', False)}")


def wait_for_execution(delay: float = 0.5):
    """Wait for order execution and notifications"""
    time.sleep(delay)


class OnlineStockExchangeDemo:
    """Comprehensive demo of the Online Stock Exchange System"""

    def __init__(self):
        self.system = StockBrokerageSystem.get_instance()

    def setup_system(self):
        """Set up the initial system with users and stocks"""
        print_separator("SYSTEM SETUP")

        # Create stocks
        print("📈 Creating Stocks...")
        self.system.add_stock(Stock("AAPL", 150.00))
        self.system.add_stock(Stock("GOOGL", 2800.00))
        self.system.add_stock(Stock("TSLA", 200.00))

        # Create users with initial balances
        print("👥 Creating Users...")
        alice = User("Alice")
        alice.get_account().credit(500000.00)  # $500,000 - Increased for testing all order types
        alice.get_account().add_stock("TSLA", 20)  # Alice owns 20 TSLA shares for testing
        self.system.register_user(alice)

        bob = User("Bob")
        bob.get_account().credit(750000.00)  # $750,000 - Increased for testing all order types
        bob.get_account().add_stock("AAPL", 100)  # Bob owns 100 AAPL shares
        self.system.register_user(bob)

        charlie = User("Charlie")
        charlie.get_account().credit(1000000.00)  # $1,000,000 - Increased for testing all order types
        charlie.get_account().add_stock("GOOGL", 20)  # Charlie owns 20 GOOGL shares
        charlie.get_account().add_stock("TSLA", 50)  # Charlie owns 50 TSLA shares
        self.system.register_user(charlie)

        # Set up observers (for all users and stocks: Observer Pattern)
        for stock in self.system.get_all_stocks().values():
            for user in self.system.get_all_users().values():
                stock.add_observer(user)

        print("✅ System setup complete!")

    def show_initial_state(self):
        """Show initial state of all users and stocks"""
        print_separator("INITIAL STATE")

        print("📊 Stock Prices:")
        for stock in self.system.get_all_stocks().values():
            print_stock_status(stock)

        print("\n👥 User Accounts:")
        for user in self.system.get_all_users().values():
            print_account_status(user)

    def demonstrate_market_orders(self):
        """Demonstrate market buy and sell orders"""
        print_separator("MARKET ORDERS DEMO")
        users = self.system.get_all_users()
        stocks = self.system.get_all_stocks()

        print("🛒 Alice places a MARKET BUY order for 10 AAPL shares")
        alice_market_buy = OrderBuilder().for_user(users["Alice"]).buy(10).with_stock(stocks["AAPL"]).as_market().build()

        print_order_details(alice_market_buy, "Alice's Market Buy Order")

        print("\n💸 Bob places a MARKET SELL order for 15 AAPL shares")
        bob_market_sell = OrderBuilder().for_user(users["Bob"]).sell(15).with_stock(stocks["AAPL"]).as_market().build()

        print_order_details(bob_market_sell, "Bob's Market Sell Order")

        # Execute orders
        print("\n⚡ Executing Market Orders...")
        self.system.place_buy_order(alice_market_buy)
        self.system.place_sell_order(bob_market_sell)

        wait_for_execution()

        print("\n📊 Results after Market Orders:")
        print_stock_status(stocks["AAPL"])
        print_account_status(users["Alice"])
        print_account_status(users["Bob"])

    def demonstrate_limit_orders(self):
        """Demonstrate limit buy and sell orders with matching"""
        print_separator("LIMIT ORDERS DEMO")
        users = self.system.get_all_users()
        stocks = self.system.get_all_stocks()

        print("🎯 Alice places a LIMIT BUY order for 20 GOOGL shares at $2750")
        alice_limit_buy = OrderBuilder().for_user(users["Alice"]).buy(20).with_stock(stocks["GOOGL"]).as_limit(2750.00).build()

        print_order_details(alice_limit_buy, "Alice's Limit Buy Order")

        print("\n🎯 Charlie places a LIMIT SELL order for 15 GOOGL shares at $2750")
        charlie_limit_sell = OrderBuilder().for_user(users["Charlie"]).sell(15).with_stock(stocks["GOOGL"]).as_limit(2750.00).build()

        print_order_details(charlie_limit_sell, "Charlie's Limit Sell Order")

        # Execute orders
        print("\n⚡ Executing Limit Orders...")
        self.system.place_buy_order(alice_limit_buy)
        self.system.place_sell_order(charlie_limit_sell)

        wait_for_execution()

        print("\n📊 Results after Limit Orders:")
        print_stock_status(stocks["GOOGL"])
        print_account_status(users["Alice"])
        print_account_status(users["Charlie"])

    def demonstrate_stop_loss_orders(self):
        """Demonstrate stop loss orders with price triggers"""
        print_separator("STOP LOSS ORDERS DEMO")
        users = self.system.get_all_users()
        stocks = self.system.get_all_stocks()
        print("🛑 Alice places a STOP LOSS BUY order for 5 TSLA shares at $210")
        print("   (Will trigger when TSLA price goes above $210)")
        alice_stop_loss_buy = OrderBuilder().for_user(users["Alice"]).buy(5).with_stock(stocks["TSLA"]).as_stop_loss(210.00).build()

        print_order_details(alice_stop_loss_buy, "Alice's Stop Loss Buy Order")

        print("\n🛑 Bob places a STOP LOSS SELL order for 10 AAPL shares at $140")
        print("   (Will trigger when AAPL price goes below $140)")
        bob_stop_loss_sell = OrderBuilder().for_user(users["Bob"]).sell(10).with_stock(stocks["AAPL"]).as_stop_loss(140.00).build()

        print_order_details(bob_stop_loss_sell, "Bob's Stop Loss Sell Order")

        # Place stop loss orders
        print("\n⚡ Placing Stop Loss Orders...")
        self.system.place_buy_order(alice_stop_loss_buy)
        self.system.place_sell_order(bob_stop_loss_sell)

        print("\n📈 Triggering Stop Loss Orders by changing stock prices...")

        # Trigger Alice's stop loss buy by increasing TSLA price
        print("   📈 TSLA price increases to $215 (triggers Alice's stop loss buy)")
        stocks["TSLA"].set_price(215.00)
        wait_for_execution()

        # Trigger Bob's stop loss sell by decreasing AAPL price
        print("   📉 AAPL price decreases to $135 (triggers Bob's stop loss sell)")
        stocks["AAPL"].set_price(135.00)
        wait_for_execution()

        print("\n📊 Results after Stop Loss Orders:")
        print_stock_status(stocks["TSLA"])
        print_stock_status(stocks["AAPL"])
        print_account_status(users["Alice"])
        print_account_status(users["Bob"])

    def demonstrate_stop_limit_orders(self):
        """Demonstrate stop limit orders with price triggers"""
        print_separator("STOP LIMIT ORDERS DEMO")
        users = self.system.get_all_users()
        stocks = self.system.get_all_stocks()
        print("🎯 Charlie places a STOP LIMIT BUY order for 8 GOOGL shares")
        print("   Stop: $2850, Limit: $2800 (triggers when GOOGL >= $2850, executes at $2800)")
        charlie_stop_limit_buy = OrderBuilder().for_user(users["Charlie"]).buy(8).with_stock(stocks["GOOGL"]).as_stop_limit(2850.00, 2800.00).build()

        print_order_details(charlie_stop_limit_buy, "Charlie's Stop Limit Buy Order")

        print("\n🎯 Alice places a STOP LIMIT SELL order for 12 TSLA shares")
        print("   Stop: $190, Limit: $195 (triggers when TSLA <= $190, executes at $195)")
        alice_stop_limit_sell = OrderBuilder().for_user(users["Alice"]).sell(12).with_stock(stocks["TSLA"]).as_stop_limit(190.00, 195.00).build()

        print_order_details(alice_stop_limit_sell, "Alice's Stop Limit Sell Order")

        # Place stop limit orders
        print("\n⚡ Placing Stop Limit Orders...")
        self.system.place_buy_order(charlie_stop_limit_buy)
        self.system.place_sell_order(alice_stop_limit_sell)

        print("\n📈 Triggering Stop Limit Orders by changing stock prices...")

        # Trigger Charlie's stop limit buy by increasing GOOGL price
        print("   📈 GOOGL price increases to $2900 (triggers Charlie's stop limit buy)")
        stocks["GOOGL"].set_price(2900.00)
        wait_for_execution()

        # Trigger Alice's stop limit sell by decreasing TSLA price
        print("   📉 TSLA price decreases to $185 (triggers Alice's stop limit sell)")
        stocks["TSLA"].set_price(185.00)
        wait_for_execution()

        print("\n📊 Results after Stop Limit Orders:")
        print_stock_status(stocks["GOOGL"])
        print_stock_status(stocks["TSLA"])
        print_account_status(users["Charlie"])
        print_account_status(users["Alice"])

    def demonstrate_order_cancellation(self):
        """Demonstrate order cancellation scenarios"""
        print_separator("ORDER CANCELLATION DEMO")
        users = self.system.get_all_users()
        stocks = self.system.get_all_stocks()
        print("❌ Alice places a LIMIT BUY order for 5 GOOGL shares at $2600")
        alice_cancel_order = OrderBuilder().for_user(users["Alice"]).buy(5).with_stock(stocks["GOOGL"]).as_limit(2600.00).build()

        print_order_details(alice_cancel_order, "Alice's Order to Cancel")

        # Place order
        print("\n⚡ Placing Order...")
        self.system.place_buy_order(alice_cancel_order)
        wait_for_execution()

        print(f"\n📋 Order Status: {alice_cancel_order.get_status().value}")

        # Cancel order
        print("\n❌ Cancelling Order...")
        self.system.cancel_order(alice_cancel_order)
        wait_for_execution()

        print(f"📋 Order Status after cancellation: {alice_cancel_order.get_status().value}")

        # Try to cancel a filled order
        print("\n❌ Trying to cancel an already FILLED order...")
        print("   (This should fail)")
        try:
            # Try to cancel Alice's limit buy order that was filled earlier
            if alice_cancel_order:
                self.system.cancel_order(alice_cancel_order)
            else:
                print("   ℹ️  No filled order available to test cancellation")
        except Exception as e:
            print(f"   ❌ Cancellation failed: {e}")

    def show_final_state(self):
        """Show final state of all users and stocks"""
        print_separator("FINAL STATE")
        users = self.system.get_all_users()
        stocks = self.system.get_all_stocks()
        print("📊 Final Stock Prices:")
        for stock in stocks.values():
            print_stock_status(stock)

        print("\n👥 Final User Accounts:")
        for user in users.values():
            print_account_status(user)

    def run_demo(self):
        """Run the complete demo"""
        print_separator("ONLINE STOCK EXCHANGE SYSTEM DEMO")
        print("This demo showcases all order types: Market, Limit, Stop Loss, and Stop Limit")

        try:
            # Setup
            self.setup_system()
            self.show_initial_state()

            # Demonstrate different order types
            self.demonstrate_market_orders()
            self.demonstrate_limit_orders()
            self.demonstrate_stop_loss_orders()
            self.demonstrate_stop_limit_orders()
            self.demonstrate_order_cancellation()

            # Final state
            self.show_final_state()

            print_separator("DEMO COMPLETED SUCCESSFULLY! 🎉")
            print("All order types have been demonstrated:")
            print("✅ Market Orders")
            print("✅ Limit Orders")
            print("✅ Stop Loss Orders")
            print("✅ Stop Limit Orders")
            print("✅ Order Cancellation")

        except Exception as e:
            print(f"\n❌ Demo failed with error: {e}")


if __name__ == "__main__":
    demo = OnlineStockExchangeDemo()
    demo.run_demo()
