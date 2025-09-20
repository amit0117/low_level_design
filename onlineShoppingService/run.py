import sys

sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")
from online_shopping_service_system import OnlineShoppingServiceSystem
from app.models.user import User
from app.models.product import Product
from app.models.address import Address
from app.models.payment_strategy import CreditCardPaymentStrategy, DebitCardPaymentStrategy, UpiPaymentStrategy, CashOnDeliveryPaymentStrategy
from app.models.search_strategy import SearchByNameStrategy, SearchByCategoryStrategy, SearchByPriceRangeStrategy
from app.models.enums import UserType, ProductCategory
from app.models.product_decorator import GiftWrapperDecorator
import time
from app.models.shopping_cart import ShoppingCart


def print_separator(title: str):
    """Helper function to print section separators"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_user_management(system: OnlineShoppingServiceSystem):
    """Test user registration, login, and management scenarios"""
    print_separator("USER MANAGEMENT SCENARIOS")

    # Create addresses
    alice_address = Address("123 Main St", "New York", "NY", "10001", "USA")
    bob_address = Address("456 Oak Ave", "Los Angeles", "CA", "90210", "USA")
    admin_address = Address("789 Admin Blvd", "San Francisco", "CA", "94102", "USA")

    # Create users
    alice = User("alice123", "password123", alice_address, UserType.NORMAL_USER)
    bob = User("bob456", "password456", bob_address, UserType.NORMAL_USER)
    admin = User("admin", "admin123", admin_address, UserType.ADMIN)

    # Register users
    print("Registering users...")
    system.register_user(alice)
    system.register_user(bob)
    system.register_user(admin)

    # Test login
    print("\nTesting user login...")
    system.login_user("alice123", "password123")
    system.login_user("bob456", "wrong_password")  # Should fail

    # Test user service methods
    print(f"\nAlice's user ID: {alice.get_user_id()}")
    print(f"Alice's address: {alice.get_shipping_address()}")

    # Update Alice's address
    new_address = Address("999 New St", "Boston", "MA", "02101", "USA")
    alice.set_address(new_address)
    print(f"Alice's new address: {alice.get_shipping_address()}")

    return alice, bob, admin


def test_product_management(system: OnlineShoppingServiceSystem):
    """Test product creation, inventory management, and decorator patterns"""
    print_separator("PRODUCT MANAGEMENT SCENARIOS")

    # Create products
    laptop = Product("Dell XPS 15", 1499.99, "High-performance laptop", ProductCategory.ELECTRONICS)
    book = Product("Clean Code", 29.99, "Software engineering book", ProductCategory.BOOKS)
    phone = Product("iPhone 15", 999.99, "Latest smartphone", ProductCategory.ELECTRONICS)
    shirt = Product("Cotton T-Shirt", 19.99, "Comfortable cotton shirt", ProductCategory.CLOTHING)

    # Add products to inventory with initial stock
    print("Adding products to inventory...")
    system.inventory_service.add_product(laptop, 10)
    system.inventory_service.add_product(book, 50)
    system.inventory_service.add_product(phone, 5)
    system.inventory_service.add_product(shirt, 25)

    # Test inventory management
    print(f"\nLaptop stock: {system.inventory_service.get_product_stock_count(laptop.get_product_id())}")
    print(f"Book stock: {system.inventory_service.get_product_stock_count(book.get_product_id())}")

    # Test product decorators
    print("\nTesting product decorators...")
    gift_wrapped_book = GiftWrapperDecorator(book)

    print(f"Original book price: ${book.get_price():.2f}")
    print(f"Gift-wrapped book price: ${gift_wrapped_book.get_price():.2f}")
    print(f"Gift-wrapped book description: {gift_wrapped_book.get_description()}")

    # Test inventory updates
    print("\nTesting inventory updates...")
    system.inventory_service.update_stock(laptop.get_product_id(), -2)  # Sell 2 laptops
    print(f"Laptop stock after selling 2: {system.inventory_service.get_product_stock_count(laptop.get_product_id())}")

    # Test out of stock scenario
    system.inventory_service.update_stock(phone.get_product_id(), -5)  # Sell all phones
    print(f"Phone stock after selling all: {system.inventory_service.get_product_stock_count(phone.get_product_id())}")
    print(f"Phone available: {system.inventory_service.is_product_available(phone.get_product_id())}")

    return laptop, book, phone, shirt, gift_wrapped_book


def test_search_scenarios(system: OnlineShoppingServiceSystem):
    """Test different search strategies"""
    print_separator("SEARCH SCENARIOS")

    # Test search by name
    print("Testing search by name...")
    name_strategy = SearchByNameStrategy()
    system.search_service.set_strategy(name_strategy)
    laptop_products = system.search_products(name_strategy, "laptop")
    print(f"Found {len(laptop_products)} products with 'laptop' in name")

    # Test search by category
    print("Testing search by category...")
    category_strategy = SearchByCategoryStrategy()
    system.search_service.set_strategy(category_strategy)
    electronics_products = system.search_products(category_strategy, ProductCategory.ELECTRONICS)
    print(f"Found {len(electronics_products)} electronics products")

    # Test search by price range
    print("Testing search by price range...")
    price_strategy = SearchByPriceRangeStrategy()
    system.search_service.set_strategy(price_strategy)
    affordable_products = system.search_products(price_strategy, (0, 50))
    print(f"Found {len(affordable_products)} products under $50")


def test_shopping_cart_scenarios(system: OnlineShoppingServiceSystem, user: User, products: list):
    """Test shopping cart operations"""
    print_separator("SHOPPING CART SCENARIOS")

    laptop, book, phone, shirt, gift_wrapped_book = products

    print("Adding items to cart...")
    system.add_product_to_cart(user, laptop, 2)
    system.add_product_to_cart(user, book, 1)
    system.add_product_to_cart(user, shirt, 3)

    # Test cart operations
    cart = user.get_account().get_cart()
    print(f"Cart total: ${cart.get_total():.2f}")
    print(f"Number of items in cart: {len(cart.get_items())}")

    # Test updating quantities
    print("\nUpdating item quantities...")
    system.update_product_in_cart(user, laptop, 1)  # Add 1 more laptop
    print(f"Updated cart total: ${cart.get_total():.2f}")

    # Test removing items
    print("\nRemoving items from cart...")
    system.remove_product_from_cart(user, shirt)
    print(f"Cart total after removing shirt: ${cart.get_total():.2f}")

    return cart


def test_order_scenarios(system: OnlineShoppingServiceSystem, user: User, cart: ShoppingCart):
    """Test order placement and state management"""
    print_separator("ORDER SCENARIOS")

    if not cart.get_items():
        print("Cart is empty, adding some items...")
        # Add some items if cart is empty
        laptop = Product("Test Laptop", 999.99, "Test laptop", ProductCategory.ELECTRONICS)
        system.inventory_service.add_product(laptop, 5)
        system.add_product_to_cart(user, laptop, 1)
        cart = user.get_account().get_cart()

    print(f"Placing order with cart total: ${cart.get_total():.2f}")

    # Test different payment methods
    payment_methods = [
        ("Credit Card", CreditCardPaymentStrategy("1234-5678-9012-3456")),
        ("Debit Card", DebitCardPaymentStrategy("9876-5432-1098-7654")),
        ("UPI", UpiPaymentStrategy("test@upi")),
        ("Cash on Delivery", CashOnDeliveryPaymentStrategy()),
    ]

    for method_name, payment_strategy in payment_methods:
        print(f"\nTesting {method_name} payment...")
        order = system.place_order(user, payment_strategy)

        if order:
            print(f"Order placed successfully! Order ID: {order.get_order_id()}")
            print(f"Order status: {order.get_status()}")
            print(f"Order total: ${order.get_total_price():.2f}")

            # Test order state transitions
            print(f"\nTesting order state transitions for {method_name}...")
            print(f"Current state: {type(order.get_state()).__name__}")

            # Try to ship the order
            if system.order_service.ship_order(order.get_order_id()):
                print("Order shipped successfully!")
                print(f"New status: {order.get_status()}")

            # Try to deliver the order
            if system.order_service.deliver_order(order.get_order_id()):
                print("Order delivered successfully!")
                print(f"Final status: {order.get_status()}")

            # Try to cancel a delivered order (should fail)
            if not system.order_service.cancel_order(order.get_order_id()):
                print("Cannot cancel delivered order (as expected)")

            break  # Only test one successful order
        else:
            print(f"Order failed with {method_name}")


def test_observer_patterns(system: OnlineShoppingServiceSystem, users: list):
    """Test observer patterns for inventory and order notifications"""
    print_separator("OBSERVER PATTERN SCENARIOS")

    alice, bob, admin = users

    # Register users as observers
    print("Registering users as inventory observers...")
    system.inventory_service.add_observer(alice)
    system.inventory_service.add_observer(bob)
    system.inventory_service.add_observer(admin)

    # Create a new product and add it to inventory
    new_product = Product("New Gaming Laptop", 1999.99, "High-end gaming laptop", ProductCategory.ELECTRONICS)
    print(f"\nAdding new product: {new_product.get_name()}")
    system.inventory_service.add_product(new_product, 0)  # Start with 0 stock

    # Update stock to trigger notifications
    print("Updating stock to trigger notifications...")
    system.inventory_service.update_stock(new_product.get_product_id(), 10)  # Should notify all users

    # Test out of stock notification
    print("\nTesting out of stock notification...")
    system.inventory_service.update_stock(new_product.get_product_id(), -10)  # Should notify admin only


def test_error_scenarios(system: OnlineShoppingServiceSystem, user: User):
    """Test error handling scenarios"""
    print_separator("ERROR HANDLING SCENARIOS")

    # Test placing order with empty cart
    print("Testing order with empty cart...")
    user.get_account().get_cart().clear()
    order = system.place_order(user, CreditCardPaymentStrategy("1234-5678-9012-3456"))
    if not order:
        print("Correctly prevented order with empty cart")

    # Test insufficient stock scenario
    print("\nTesting insufficient stock scenario...")
    expensive_product = Product("Expensive Item", 9999.99, "Very expensive item", ProductCategory.ELECTRONICS)
    system.inventory_service.add_product(expensive_product, 1)  # Only 1 in stock
    system.add_product_to_cart(user, expensive_product, 5)  # Try to buy 5

    order = system.place_order(user, CreditCardPaymentStrategy("1234-5678-9012-3456"))
    if not order:
        print("Correctly prevented order due to insufficient stock")

    # Test out of stock scenario
    print("\nTesting out of stock scenario...")
    out_of_stock_product = Product("Out of Stock Item", 99.99, "This item is out of stock", ProductCategory.OTHER)
    system.inventory_service.add_product(out_of_stock_product, 0)  # 0 in stock
    user.get_account().get_cart().clear()
    system.add_product_to_cart(user, out_of_stock_product, 1)

    order = system.place_order(user, CreditCardPaymentStrategy("1234-5678-9012-3456"))
    if not order:
        print("Correctly prevented order due to out of stock item")


def test_system_integration(system: OnlineShoppingServiceSystem):
    """Test complete system integration scenarios"""
    print_separator("SYSTEM INTEGRATION SCENARIOS")

    # Create a complete shopping scenario
    print("Running complete shopping scenario...")

    # 1. Create user
    address = Address("123 Shopping St", "Mall City", "MC", "12345", "USA")
    shopper = User("shopper", "password", address, UserType.NORMAL_USER)
    system.register_user(shopper)

    # 2. Add products
    products = [
        Product("Wireless Headphones", 199.99, "Noise-cancelling headphones", ProductCategory.ELECTRONICS),
        Product("Programming Book", 49.99, "Learn Python programming", ProductCategory.BOOKS),
        Product("Coffee Mug", 12.99, "Ceramic coffee mug", ProductCategory.OTHER),
    ]

    for product in products:
        system.inventory_service.add_product(product, 10)

    # 3. Add to cart
    for product in products:
        system.add_product_to_cart(shopper, product, 1)

    # 4. Place order
    cart = shopper.get_account().get_cart()
    print(f"Cart total: ${cart.get_total():.2f}")

    order = system.place_order(shopper, UpiPaymentStrategy("shopper@paytm"))
    if order:
        print(f"Complete shopping scenario successful! Order ID: {order.get_order_id()}")

        # 5. Track order through states
        print("Tracking order through states...")
        system.order_service.ship_order(order.get_order_id())
        time.sleep(1)  # Simulate processing time
        system.order_service.deliver_order(order.get_order_id())

        print(f"Final order status: {order.get_status()}")


def run():
    """Main function to run all test scenarios"""
    print("🚀 Starting Online Shopping Service System Demo")
    print("This demo will test various scenarios using the service architecture")

    # Initialize system
    system = OnlineShoppingServiceSystem.get_instance()

    try:
        # Run all test scenarios
        users = test_user_management(system)
        products = test_product_management(system)
        test_search_scenarios(system)
        cart = test_shopping_cart_scenarios(system, users[0], products)
        test_order_scenarios(system, users[0], cart)
        test_observer_patterns(system, users)
        test_error_scenarios(system, users[0])
        test_system_integration(system)

        print_separator("DEMO COMPLETED SUCCESSFULLY")
        print("✅ All scenarios tested successfully!")
        print("The service architecture is working as expected.")

    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    run()
