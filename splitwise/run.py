from app.services.split_wise_service import SplitWiseService

from app.strategies.split_strategy import EqualSplitStrategy, PercentSplitStrategy, ExactSplitStrategy
from app.builders.expense_builder import ExpenseBuilder

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


class SplitwiseDemo:
    @staticmethod
    def main():
        print("=" * 60)
        print("🚀 SPLITWISE SYSTEM DEMO - Design Patterns Showcase")
        print("=" * 60)

        # 1. Setup the service (Singleton Pattern)
        print("\n📋 STEP 1: Initializing SplitWise Service (Singleton Pattern)")
        print("-" * 50)
        service = SplitWiseService.get_instance()
        service2 = SplitWiseService.get_instance()
        print(f"✅ Singleton verified: service == service2: {service is service2}")

        # 2. Create users with profile management
        print("\n👥 STEP 2: User Account Creation & Profile Management")
        print("-" * 50)
        print("💡 Demonstrating: User account creation and profile management")

        arjun = service.add_user("Arjun Sharma", "arjun@email.com")
        priya = service.add_user("Priya Patel", "priya@email.com")
        rahul = service.add_user("Rahul Kumar", "rahul@email.com")
        sneha = service.add_user("Sneha Gupta", "sneha@email.com")
        vikram = service.add_user("Vikram Singh", "vikram@email.com")

        print(f"✅ Created user accounts:")
        for user in [arjun, priya, rahul, sneha, vikram]:
            print(f"   👤 {user.get_name()} ({user.get_email()}) - ID: {user.get_id()[:8]}...")

        print(f"\n📋 Profile Information Available:")
        print(f"   • Name: {arjun.get_name()}")
        print(f"   • Email: {arjun.get_email()}")
        print(f"   • User ID: {arjun.get_id()}")
        print(f"   • Balance Sheet: {type(arjun.get_balance_sheet()).__name__}")

        # 3. Comprehensive Group Management
        print("\n🏠 STEP 3: Comprehensive Group Management")
        print("-" * 50)
        print("💡 Demonstrating: Group creation, member management, and group operations")

        vacation_group = service.add_group("Goa Trip", [arjun, priya, rahul, sneha])
        office_group = service.add_group("Office Lunch", [priya, rahul, vikram])

        print(f"✅ Created groups:")
        print(f"   🏖️ {vacation_group.get_name()} - Members: {len(vacation_group.get_members())}")
        print(f"   🍕 {office_group.get_name()} - Members: {len(office_group.get_members())}")

        print(f"\n👥 Group Member Management:")
        print(f"   {vacation_group.get_name()} members:")
        for member in vacation_group.get_members():
            print(f"     • {member.get_name()}")

        print(f"   {office_group.get_name()} members:")
        for member in office_group.get_members():
            print(f"     • {member.get_name()}")

        # 4. Scenario 1: Equal Split (Strategy Pattern + Builder Pattern + Clean Observer Pattern)
        print("\n🍽️ SCENARIO 1: Equal Split - Restaurant Dinner")
        print("-" * 50)
        print("💡 Demonstrating: Strategy Pattern (EqualSplitStrategy) + Builder Pattern (ExpenseBuilder) + Clean Observer Pattern")
        print("📢 Only participants (Arjun, Priya, Rahul, Sneha) will be notified via expense_update() method")

        dinner_expense = (
            ExpenseBuilder()
            .set_description("Fine Dining at Taj Hotel")
            .set_amount(4000.0)
            .set_paid_by(arjun)
            .set_participants([arjun, priya, rahul, sneha])
            .set_split_strategy(EqualSplitStrategy())
            .build()
        )

        service.add_expense_to_group(vacation_group.get_id(), dinner_expense)
        print("✅ Equal split expense added - Clean Observer Pattern in action!")

        # 5. Scenario 2: Exact Split
        print("\n🎬 SCENARIO 2: Exact Split - Movie Tickets")
        print("-" * 50)
        print("💡 Demonstrating: Strategy Pattern (ExactSplitStrategy) + Clean Observer Pattern")
        print("📢 Only participants (Arjun, Priya, Rahul) will be notified via expense_update() - Sneha is NOT involved!")

        movie_expense = (
            ExpenseBuilder()
            .set_description("Movie Tickets at PVR")
            .set_amount(1500.0)
            .set_paid_by(priya)
            .set_participants([arjun, priya, rahul])
            .set_split_strategy(ExactSplitStrategy())
            .set_split_values([500.0, 600.0, 400.0])
            .build()
        )

        service.add_expense_to_group(vacation_group.get_id(), movie_expense)
        print("✅ Exact split expense added - Clean Observer Pattern working perfectly!")

        # 6. Scenario 3: Percentage Split
        print("\n🛒 SCENARIO 3: Percentage Split - Grocery Shopping")
        print("-" * 50)
        print("💡 Demonstrating: Strategy Pattern (PercentSplitStrategy) + Clean Observer Pattern")
        print("📢 Only participants (Arjun, Priya, Rahul, Sneha) will be notified via expense_update()")

        grocery_expense = (
            ExpenseBuilder()
            .set_description("Grocery Shopping at Big Bazaar")
            .set_amount(3000.0)
            .set_paid_by(rahul)
            .set_participants([arjun, priya, rahul, sneha])
            .set_split_strategy(PercentSplitStrategy())
            .set_split_values([25.0, 25.0, 30.0, 20.0])
            .build()
        )

        service.add_expense_to_group(vacation_group.get_id(), grocery_expense)
        print("✅ Percentage split expense added - Clean Observer Pattern demonstrating DRY principle!")

        # 7. Scenario 4: Office Group Expense
        print("\n🍕 SCENARIO 4: Office Lunch Group")
        print("-" * 40)

        lunch_expense = (
            ExpenseBuilder()
            .set_description("Office Biryani Lunch")
            .set_amount(750.0)
            .set_paid_by(vikram)
            .set_participants([priya, rahul, vikram])
            .set_split_strategy(EqualSplitStrategy())
            .build()
        )

        service.add_expense_to_group(office_group.get_id(), lunch_expense)
        print("✅ Office lunch expense added!")

        # 8. Show individual balance sheets
        print("\n💰 STEP 4: Individual Balance Sheets")
        print("-" * 40)
        for user in [arjun, priya, rahul, sneha, vikram]:
            print(f"\n--- {user.get_name()}'s Balance Sheet ---")
            service.show_user_balance_sheet(user.get_id())

        # 9. Debt Simplification Algorithm Demo
        print("\n🔄 STEP 5: Debt Simplification Algorithm")
        print("-" * 45)
        print("💡 Demonstrating: Complex algorithm to minimize transactions")

        print("\n--- Goa Trip Group Debt Simplification ---")
        simplified_transactions = vacation_group.simplify_expenses()

        if not simplified_transactions:
            print("🎉 All debts are settled within the Goa trip group!")
        else:
            print(f"📊 Simplified {len(vacation_group.get_expenses())} expenses into {len(simplified_transactions)} transactions:")
            for i, transaction in enumerate(simplified_transactions, 1):
                print(f"  {i}. {transaction.get_from_user().get_name()} → {transaction.get_to_user().get_name()}: ₹{transaction.get_amount():.2f}")

        print("\n--- Office Group Debt Simplification ---")
        office_simplified = office_group.simplify_expenses()
        if not office_simplified:
            print("🎉 All debts are settled within the office group!")
        else:
            for i, transaction in enumerate(office_simplified, 1):
                print(f"  {i}. {transaction.get_from_user().get_name()} → {transaction.get_to_user().get_name()}: ₹{transaction.get_amount():.2f}")

        # 10. Comprehensive Settlement Demo with Partial Settlements
        print("\n💸 STEP 6: Comprehensive Settlement Demo")
        print("-" * 50)
        print("💡 Demonstrating: Individual balance viewing, partial settlements, and full settlements")

        print("\n📊 Current Balances Before Settlement:")
        for user in [arjun, priya, rahul, sneha, vikram]:
            print(f"\n--- {user.get_name()}'s Balance Sheet ---")
            service.show_user_balance_sheet(user.get_id())

        print("\n🔄 Partial Settlement Demo:")
        print("Step 1: Priya settles ₹500 with Arjun (partial payment)...")
        service.settle_up(priya.get_id(), arjun.get_id(), 500.0)

        print("\nStep 2: Rahul settles ₹200 with Priya (partial payment)...")
        service.settle_up(rahul.get_id(), priya.get_id(), 200.0)

        print("\nStep 3: Sneha settles ₹100 with Rahul (partial payment)...")
        service.settle_up(sneha.get_id(), rahul.get_id(), 100.0)

        print("\n📊 Balances After Partial Settlements:")
        for user in [arjun, priya, rahul, sneha]:
            print(f"\n--- {user.get_name()}'s Updated Balance Sheet ---")
            service.show_user_balance_sheet(user.get_id())

        print("\n💰 Full Settlement Demo:")
        print("Step 4: Complete settlement between Priya and Arjun...")
        # Get remaining balance and settle completely
        arjun_balance = arjun.get_balance_sheet().get_balances()
        if priya in arjun_balance:
            remaining_amount = arjun_balance[priya]
            if remaining_amount > 0:
                service.settle_up(priya.get_id(), arjun.get_id(), remaining_amount)
                print(f"Settled remaining ₹{remaining_amount:.2f}")

        print("\n📊 Final Balances After Full Settlement:")
        service.show_user_balance_sheet(priya.get_id())
        service.show_user_balance_sheet(arjun.get_id())

        # 11. Group Management Demo
        print("\n👥 STEP 7: Group Management Demo")
        print("-" * 35)
        print("💡 Demonstrating: Adding/removing members (Clean Observer Pattern with update_group() method)")

        print(f"\nAdding {vikram.get_name()} to Goa trip group...")
        vacation_group.add_member(vikram)

        print(f"\nRemoving {sneha.get_name()} from Goa trip group...")
        vacation_group.remove_member(sneha)

        # 12. Transaction History Demo
        print("\n📜 STEP 8: Transaction History & Group Expenses")
        print("-" * 50)
        print("💡 Demonstrating: Transaction history viewing and group expense tracking")

        print(f"\n📋 {vacation_group.get_name()} Expense History:")
        expenses = vacation_group.get_expenses()
        for i, expense in enumerate(expenses, 1):
            print(f"   {i}. {expense.get_description()}")
            print(f"      💵 Amount: ₹{expense.get_amount():.2f}")
            print(f"      👤 Paid by: {expense.get_paid_by().get_name()}")
            print(f"      👥 Participants: {', '.join([p.get_name() for p in expense.get_participants()])}")
            print(f"      📅 Created: {expense.get_created_at()}")
            print(f"      🔄 Split Strategy: {expense.get_split_strategy().__class__.__name__}")
            print()

        print(f"\n📋 {office_group.get_name()} Expense History:")
        office_expenses = office_group.get_expenses()
        for i, expense in enumerate(office_expenses, 1):
            print(f"   {i}. {expense.get_description()}")
            print(f"      💵 Amount: ₹{expense.get_amount():.2f}")
            print(f"      👤 Paid by: {expense.get_paid_by().get_name()}")
            print(f"      👥 Participants: {', '.join([p.get_name() for p in expense.get_participants()])}")
            print(f"      📅 Created: {expense.get_created_at()}")
            print()

        # 13. Concurrent Transactions Demo with ThreadPoolExecutor
        print("\n⚡ STEP 9: Concurrent Transactions Demo")
        print("-" * 50)
        print("💡 Demonstrating: Concurrent transactions with ThreadPoolExecutor for data consistency")

        def concurrent_expense_creation(expense_data):
            """Function to create expenses concurrently"""
            thread_id = threading.current_thread().ident
            print(f"🔄 Thread {thread_id}: Creating expense - {expense_data['description']}")

            expense = (
                ExpenseBuilder()
                .set_description(expense_data["description"])
                .set_amount(expense_data["amount"])
                .set_paid_by(expense_data["paid_by"])
                .set_participants(expense_data["participants"])
                .set_split_strategy(expense_data["strategy"])
                .build()
            )

            service.add_expense_to_group(expense_data["group_id"], expense)
            print(f"✅ Thread {thread_id}: Successfully added {expense_data['description']}")
            return expense

        def concurrent_settlement(settlement_data):
            """Function to perform settlements concurrently"""
            thread_id = threading.current_thread().ident
            print(
                f"💰 Thread {thread_id}: Settling ₹{settlement_data['amount']} between {settlement_data['from_user'].get_name()} and {settlement_data['to_user'].get_name()}"
            )

            service.settle_up(settlement_data["from_user"].get_id(), settlement_data["to_user"].get_id(), settlement_data["amount"])
            print(f"✅ Thread {thread_id}: Settlement completed")
            return True

        # Prepare concurrent tasks
        concurrent_expenses = [
            {
                "description": "Concurrent Dinner",
                "amount": 800.0,
                "paid_by": arjun,
                "participants": [arjun, priya, rahul],
                "strategy": EqualSplitStrategy(),
                "group_id": vacation_group.get_id(),
            },
            {
                "description": "Concurrent Snacks",
                "amount": 300.0,
                "paid_by": priya,
                "participants": [priya, rahul, sneha],
                "strategy": EqualSplitStrategy(),
                "group_id": vacation_group.get_id(),
            },
            {
                "description": "Concurrent Coffee",
                "amount": 150.0,
                "paid_by": rahul,
                "participants": [rahul, vikram],
                "strategy": EqualSplitStrategy(),
                "group_id": office_group.get_id(),
            },
        ]

        concurrent_settlements = [
            {"from_user": priya, "to_user": arjun, "amount": 100.0},
            {"from_user": rahul, "to_user": priya, "amount": 50.0},
            {"from_user": sneha, "to_user": rahul, "amount": 75.0},
        ]

        print("\n🚀 Executing Concurrent Expense Creation:")
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Submit expense creation tasks
            expense_futures = [executor.submit(concurrent_expense_creation, expense_data) for expense_data in concurrent_expenses]

            # Wait for all expenses to complete
            for future in as_completed(expense_futures):
                try:
                    expense = future.result()
                    print(f"📝 Expense created: {expense.get_description()}")
                except Exception as e:
                    print(f"❌ Error creating expense: {e}")

        print("\n🚀 Executing Concurrent Settlements:")
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Submit settlement tasks
            settlement_futures = [executor.submit(concurrent_settlement, settlement_data) for settlement_data in concurrent_settlements]

            # Wait for all settlements to complete
            for future in as_completed(settlement_futures):
                try:
                    result = future.result()
                    print(f"✅ Settlement completed successfully")
                except Exception as e:
                    print(f"❌ Error in settlement: {e}")

        print("\n📊 Final Balances After Concurrent Operations:")
        for user in [arjun, priya, rahul, sneha, vikram]:
            print(f"\n--- {user.get_name()}'s Final Balance Sheet ---")
            service.show_user_balance_sheet(user.get_id())

        # 14. Clean Observer Pattern Showcase
        print("\n🎨 STEP 10: Clean Observer Pattern Architecture")
        print("-" * 50)
        print("💡 Your Implementation Highlights:")
        print("   ✅ DRY Principle: Single base Subject class")
        print("   ✅ Method-specific observers: expense_update(), transaction_update(), update_group()")
        print("   ✅ No code duplication: All observers inherit from base_observer.Subject")
        print("   ✅ Clean separation: Each observer type has its own dedicated method")
        print("   ✅ Type safety: Direct method calls without runtime type checking")
        print("   ✅ Maintainable: Easy to extend with new observer types")

        # 15. Final Summary
        print("\n📊 FINAL SUMMARY")
        print("=" * 30)
        print("✅ Design Patterns Demonstrated:")
        print("   • Singleton Pattern: SplitWiseService")
        print("   • Builder Pattern: ExpenseBuilder")
        print("   • Strategy Pattern: Split strategies (Equal, Exact, Percent)")
        print("   • Clean Observer Pattern: Method-specific notifications (expense_update, transaction_update, update_group)")
        print("   • Facade Pattern: SplitWiseService coordinating other services")

        print("\n✅ Features Demonstrated:")
        print("   • User account creation and profile management")
        print("   • Comprehensive group management (create, add/remove members)")
        print("   • Multiple split strategies (Equal, Exact, Percentage)")
        print("   • Automatic expense splitting among participants")
        print("   • Individual balance viewing and tracking")
        print("   • Partial and full settlement capabilities")
        print("   • Transaction history and group expense tracking")
        print("   • Concurrent transactions with ThreadPoolExecutor")
        print("   • Data consistency in multi-threaded environment")
        print("   • Clean Observer Pattern with DRY principle")

        print("\n🎯 System Architecture:")
        print("   • Clean separation of concerns")
        print("   • Service layer architecture")
        print("   • Domain-driven design")
        print("   • DRY principle implementation")
        print("   • Method-specific Observer pattern")
        print("   • Thread-safe operations with locks")
        print("   • Concurrent transaction handling")
        print("   • Data consistency guarantees")

        print("\n" + "=" * 60)
        print("🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)


def run():
    SplitwiseDemo.main()


if __name__ == "__main__":
    run()
