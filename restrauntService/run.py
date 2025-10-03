#!/usr/bin/env python3
"""
Restaurant Management System Demo
This demo showcases the complete end-to-end restaurant operations using various design patterns.
"""

from restraunt_management_app import RestrauntManagementApp
from app.models.staff import Manager, Chef, Waiter
from app.models.table import Table
from app.models.item import VegItem, NonVegItem
from app.models.order_item import OrderItem
from app.models.enums import PaymentStatus
from app.strategies.payment_strategy import CreditCardPayment, UpiPayment, CashPayment
import time


class RestaurantManagementSystemDemo:
    @staticmethod
    def main():
        print("=" * 60)
        print("RESTAURANT MANAGEMENT SYSTEM DEMO")
        print("=" * 60)

        # Initialize the restaurant management system (Singleton)
        print("\n1. Initializing Restaurant Management System...")
        rms = RestrauntManagementApp.get_instance()

        # Setup restaurant infrastructure
        RestaurantManagementSystemDemo.setup_restaurant(rms)

        # Run complete restaurant workflow
        RestaurantManagementSystemDemo.run_complete_workflow(rms)

        print("\n" + "=" * 60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    @staticmethod
    def setup_restaurant(rms: RestrauntManagementApp):
        """Setup restaurant with staff, tables, menu, and inventory"""
        print("\n2. Setting up Restaurant Infrastructure...")

        # Add staff
        manager = Manager("John Manager")
        chef1 = Chef("Gordon Chef")
        chef2 = Chef("Julia Chef")
        waiter1 = Waiter("Alice Waiter")
        waiter2 = Waiter("Bob Waiter")

        rms.add_manager(manager)
        rms.add_chef(chef1)
        rms.add_chef(chef2)
        rms.add_waiter(waiter1)
        rms.add_waiter(waiter2)

        # Add tables
        for i in range(1, 6):
            table = Table(i, 4)
            rms.add_table(table)

        # Add menu items
        pizza = VegItem("Margherita Pizza", 299.0)
        pasta = VegItem("Carbonara Pasta", 349.0)
        burger = NonVegItem("Chicken Burger", 199.0)
        fries = VegItem("French Fries", 99.0)
        coke = VegItem("Coca Cola", 49.0)
        coffee = VegItem("Cappuccino", 79.0)

        rms.add_item_to_menu(pizza)
        rms.add_item_to_menu(pasta)
        rms.add_item_to_menu(burger)
        rms.add_item_to_menu(fries)
        rms.add_item_to_menu(coke)
        rms.add_item_to_menu(coffee)

        # Add inventory
        rms.add_item_to_inventory(pizza, 20)
        rms.add_item_to_inventory(pasta, 15)
        rms.add_item_to_inventory(burger, 25)
        rms.add_item_to_inventory(fries, 30)
        rms.add_item_to_inventory(coke, 50)
        rms.add_item_to_inventory(coffee, 40)

        print("✓ Restaurant setup completed!")
        print(f"✓ Added {len(rms.get_chefs())} chefs, {len(rms.get_waiters())} waiters")
        print(f"✓ Added {len(rms.get_tables())} tables")
        print(f"✓ Added {len(rms.get_menu().get_all_items())} menu items")

    @staticmethod
    def run_complete_workflow(rms: RestrauntManagementApp):
        """Run complete restaurant workflow from customer arrival to payment"""
        print("\n3. Running Complete Restaurant Workflow...")

        # Scenario 1: Customer arrives and reserves table
        print("\n--- SCENARIO 1: Customer Arrival & Table Reservation ---")

        # Reserve and occupy tables
        success1 = rms.reserve_table(1, "Alice", 2)
        if success1:
            rms.occupy_table(1)

        success2 = rms.reserve_table(2, "Bob", 4)
        if success2:
            rms.occupy_table(2)

        # Scenario 2: Customers place orders
        print("\n--- SCENARIO 2: Order Placement ---")

        # Alice's order - create OrderItem objects
        alice_order_items = [
            OrderItem("", rms.get_menu().get_all_items()[0], 1),  # Pizza
            OrderItem("", rms.get_menu().get_all_items()[3], 1),  # Fries
            OrderItem("", rms.get_menu().get_all_items()[4], 2),  # Coke
        ]

        try:
            alice_order = rms.create_order_with_items(1, "Alice", alice_order_items)
            print(f"✓ Alice's order created: {alice_order.get_order_id()}")
        except Exception as e:
            print(f"✗ Error creating Alice's order: {e}")
            alice_order = None

        # Bob's order
        bob_order_items = [
            OrderItem("", rms.get_menu().get_all_items()[2], 2),  # Burger
            OrderItem("", rms.get_menu().get_all_items()[1], 1),  # Pasta
            OrderItem("", rms.get_menu().get_all_items()[5], 1),  # Coffee
        ]

        try:
            bob_order = rms.create_order_with_items(2, "Bob", bob_order_items)
            print(f"✓ Bob's order created: {bob_order.get_order_id()}")
        except Exception as e:
            print(f"✗ Error creating Bob's order: {e}")
            bob_order = None

        # Scenario 3: Kitchen processing
        print("\n--- SCENARIO 3: Kitchen Processing ---")

        if alice_order:
            print(f"Processing Alice's order: {alice_order.get_order_id()}")
            rms.process_order(alice_order.get_order_id())
            time.sleep(1)  # Simulate preparation time
            rms.mark_order_items_ready(alice_order.get_order_id())
            time.sleep(1)  # Simulate serving time
            rms.serve_order(alice_order.get_order_id())

        if bob_order:
            print(f"Processing Bob's order: {bob_order.get_order_id()}")
            rms.process_order(bob_order.get_order_id())
            time.sleep(1)  # Simulate preparation time
            rms.mark_order_items_ready(bob_order.get_order_id())
            time.sleep(1)  # Simulate serving time
            rms.serve_order(bob_order.get_order_id())

        # Scenario 4: Bill generation and payment
        print("\n--- SCENARIO 4: Bill Generation & Payment ---")

        if alice_order:
            print("\nGenerating bill for Alice's order...")
            rms.generate_bill(alice_order.get_order_id(), tax_rate=0.18, service_charge=50.0)

            # Process payment using UPI
            upi_payment = UpiPayment()
            payment_result = rms.process_payment(upi_payment, 500.0)
            print(f"Payment status: {payment_result.get_status().value}")

            if payment_result.get_status() == PaymentStatus.SUCCESS:
                rms.release_table(1)
                print("✓ Alice's table released")

        if bob_order:
            print("\nGenerating bill for Bob's order...")
            rms.generate_bill(bob_order.get_order_id(), tax_rate=0.18, service_charge=50.0, discount_percentage=10.0)

            # Process payment using Credit Card
            credit_payment = CreditCardPayment()
            payment_result = rms.process_payment(credit_payment, 800.0)
            print(f"Payment status: {payment_result.get_status().value}")

            if payment_result.get_status() == PaymentStatus.SUCCESS:
                rms.release_table(2)
                print("✓ Bob's table released")

        # Scenario 5: Additional customer with different payment method
        print("\n--- SCENARIO 5: Additional Customer (Cash Payment) ---")

        # Reserve and occupy table 3
        success3 = rms.reserve_table(3, "Charlie Customer", 2)
        if success3:
            rms.occupy_table(3)

        # Charlie's order
        charlie_order_items = [
            OrderItem("", rms.get_menu().get_all_items()[0], 1),
            OrderItem("", rms.get_menu().get_all_items()[5], 2),
        ]  # Pizza  # Coffee

        try:
            charlie_order = rms.create_order_with_items(3, "Charlie Customer", charlie_order_items)
            print(f"✓ Charlie's order created: {charlie_order.get_order_id()}")

            # Process Charlie's order
            rms.process_order(charlie_order.get_order_id())
            time.sleep(1)
            rms.mark_order_items_ready(charlie_order.get_order_id())
            time.sleep(1)
            rms.serve_order(charlie_order.get_order_id())

            # Generate bill and process payment
            rms.generate_bill(charlie_order.get_order_id(), tax_rate=0.18, service_charge=50.0)

            # Process payment using Cash
            cash_payment = CashPayment()
            payment_result = rms.process_payment(cash_payment, 400.0)
            print(f"Payment status: {payment_result.get_status().value}")

            if payment_result.get_status() == PaymentStatus.SUCCESS:
                rms.release_table(3)
                print("✓ Charlie's table released")

        except Exception as e:
            print(f"✗ Error processing Charlie's order: {e}")

        # Scenario 6: Edge Cases
        print("\n--- SCENARIO 6: Edge Cases ---")

        # Test out-of-stock
        rms.occupy_table(4)
        try:
            rms.create_order_with_items(4, "David Customer", [OrderItem("", rms.get_menu().get_all_items()[0], 50)])  # Order more than available
        except Exception as e:
            print(f"✓ Out-of-stock handled: {type(e).__name__}")

        # Test table not occupied
        try:
            rms.create_order_with_items(5, "Eve Customer", [OrderItem("", rms.get_menu().get_all_items()[0], 1)])
        except Exception as e:
            print(f"✓ Table validation: {type(e).__name__}")

        # Test payment failure
        class FailingPayment:
            def pay(self, amount: float):
                from app.models.payment import Payment
                from app.models.enums import PaymentMethod, PaymentStatus

                return Payment(amount, PaymentMethod.CREDIT_CARD, PaymentStatus.FAILED)

        payment_result = rms.process_payment(FailingPayment(), 100.0)
        print(f"✓ Payment failure handled: {payment_result.get_status().value}")

        # Final status
        print(f"\nFinal Status: {len(rms.get_available_tables())} tables available, {len(rms.get_orders())} orders processed")

        # Design patterns
        print("\n--- DESIGN PATTERNS ---")
        print("✓ Repository, Service, Facade, Singleton, Observer, State, Command, Decorator, Strategy")


if __name__ == "__main__":
    RestaurantManagementSystemDemo.main()
