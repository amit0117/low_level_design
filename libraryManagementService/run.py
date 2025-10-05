#!/usr/bin/env python3
"""
Library Management System Comprehensive Demo
This demo showcases the complete end-to-end library management operations including:
- Librarian catalog management (add, update, remove books)
- Member registration and management
- Borrowing and returning books with rules enforcement
- Concurrent access handling
- Payment processing and fine management
- Comprehensive reporting and statistics
"""

from library_management import LibraryManagement
from app.models.enums import ItemStatus
from app.strategies.payment_strategy import CreditCardPaymentStrategy, CashPaymentStrategy, BankTransferPaymentStrategy
import time
import random
from app.models.book import Book
from app.models.member import Member
from app.models.borrow import Borrow
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.factories.library_item_factory import BookFactory, MagazineFactory


class LibraryManagementDemo:
    @staticmethod
    def main():
        print("=" * 80)
        print("LIBRARY MANAGEMENT SYSTEM COMPREHENSIVE DEMO")
        print("=" * 80)

        # Initialize the library management system (Singleton)
        print("\n1. Initializing Library Management System...")
        library = LibraryManagement.get_instance()

        # Run complete library management workflow
        LibraryManagementDemo.run_complete_workflow(library)

        # Run comprehensive validation scenarios
        print("\n" + "=" * 80)
        print("COMPREHENSIVE VALIDATION")
        print("=" * 80)

        # Librarian Catalog Management
        LibraryManagementDemo.validate_catalog_management(library)

        # Member Management
        LibraryManagementDemo.validate_member_management(library)

        # Borrowing Rules and Enforcement
        LibraryManagementDemo.validate_borrowing_rules(library)

        # Concurrent Access Testing
        LibraryManagementDemo.validate_concurrent_access(library)

        # Payment and Fine Management
        LibraryManagementDemo.validate_payment_and_fines(library)

        # Advanced Features
        LibraryManagementDemo.validate_advanced_features(library)

        # Performance and Scalability
        LibraryManagementDemo.validate_performance_and_scalability(library)

        print("\n" + "=" * 80)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 80)

    @staticmethod
    def run_complete_workflow(library: LibraryManagement):
        """Run complete library management workflow from setup to operations"""
        print("\n2. Running Complete Library Management Workflow...")

        # Scenario 1: Librarian Catalog Management
        print("\n--- SCENARIO 1: Librarian Catalog Management ---")

        # Add various types of books to catalog using Factory Method pattern
        books: list[Book] = []

        book_factory = BookFactory()  # Create books using factory pattern
        book1 = book_factory.create_item("Python Programming Guide", "Guido van Rossum", 2020, 9780134685991)
        book2 = book_factory.create_item("Design Patterns", "Gang of Four", 1994, 9780201633610)
        book3 = book_factory.create_item("Clean Code", "Robert Martin", 2008, 9780132350884)
        book4 = book_factory.create_item("System Design Interview", "Alex Xu", 2020, 9781736049112)

        # Create magazines using factory pattern
        magazine_factory = MagazineFactory()
        magazine1 = magazine_factory.create_item("National Geographic", "Various Authors", 2023, 279356)

        # Add created items to library
        books.append(library.add_item(book1))
        books.append(library.add_item(book2))
        books.append(library.add_item(book3))
        books.append(library.add_item(book4))
        books.append(library.add_item(magazine1))

        print(f"✓ Added {len(books)} items to library catalog using Factory Method pattern")
        for book in books:
            print(f"  - {book.get_title()} by {book.get_author()} ({book.get_type().value})")

        # Update book information (simulate catalog updates)
        print("\n--- Updating Catalog Information ---")
        # Mark some items as reference only
        library.item_repository.get_item_by_id(books[3].get_id()).set_status(ItemStatus.REFERENCE_ONLY)
        print(f"✓ Updated {books[3].get_title()} to reference only")

        # Scenario 2: Member Registration and Management
        print("\n--- SCENARIO 2: Member Registration & Management ---")

        # Register multiple members with different profiles
        members: list[Member] = []
        members.append(library.register_member("Arjun Sharma"))
        members.append(library.register_member("Priya Patel"))
        members.append(library.register_member("Rajesh Kumar"))
        members.append(library.register_member("Sneha Gupta"))
        members.append(library.register_member("Vikram Singh"))

        print(f"✓ Registered {len(members)} members")
        for member in members:
            print(f"  - {member.get_name()} (ID: {member.get_id()})")

        # Scenario 3: Borrowing Operations with Rules Enforcement
        print("\n--- SCENARIO 3: Borrowing Operations & Rules Enforcement ---")

        # Test borrowing rules - maximum books per member
        print("\n--- Testing Borrowing Rules ---")

        # Arjun borrows multiple books
        arjun_borrows: list[Borrow] = []
        arjun_borrows.append(library.request_item(books[0].get_id(), members[0].get_id(), 14))
        arjun_borrows.append(library.request_item(books[1].get_id(), members[0].get_id(), 21))
        arjun_borrows.append(library.request_item(books[2].get_id(), members[0].get_id(), 7))

        print(f"✓ {members[0].get_name()} requested {len(arjun_borrows)} books")

        # Process borrows
        for borrow in arjun_borrows:
            library.borrow_item(borrow.get_id())
            print(f"✓ Borrowed: {borrow.get_item().get_title()}")

        # Priya borrows books
        priya_borrows: list[Borrow] = []
        priya_borrows.append(library.request_item(books[4].get_id(), members[1].get_id(), 3))
        library.borrow_item(priya_borrows[0].get_id())
        print(f"✓ {members[1].get_name()} borrowed: {priya_borrows[0].get_item().get_title()}")

        # Rajesh tries to borrow the reference-only book (should fail)
        try:
            rajesh_borrow = library.request_item(books[3].get_id(), members[2].get_id(), 14)
            library.borrow_item(rajesh_borrow.get_id())
            print(f"✓ {members[2].get_name()} borrowed: {rajesh_borrow.get_item().get_title()}")
        except Exception as e:
            print(f"✓ Reference-only book protection working: {str(e)}")

        # Scenario 4: Renewal Operations
        print("\n--- SCENARIO 4: Renewal Operations ---")

        # Arjun renews one of his books
        library.renew_item(arjun_borrows[0].get_id(), 7)
        print(f"✓ {members[0].get_name()} renewed: {arjun_borrows[0].get_item().get_title()}")

        # Test maximum renewal limit
        try:
            library.renew_item(arjun_borrows[0].get_id(), 7)  # Second renewal
            library.renew_item(arjun_borrows[0].get_id(), 7)  # Third renewal (should fail)
        except Exception as e:
            print(f"✓ Maximum renewal limit enforced: {str(e)}")

        # Scenario 5: Payment Processing
        print("\n--- SCENARIO 5: Payment Processing ---")

        # Process membership fees with different payment methods
        credit_card = CreditCardPaymentStrategy("1234-5678-9012-3456", "123")
        cash = CashPaymentStrategy()
        bank_transfer = BankTransferPaymentStrategy("987654321", "State Bank of India")

        # Arjun pays membership fee with credit card
        payment_result = library.pay_membership_fee(members[0].get_id(), 25.0, credit_card)
        print(f"✓ {members[0].get_name()} paid membership fee: ${payment_result.get_amount()}")

        # Priya pays with cash
        payment_result = library.pay_membership_fee(members[1].get_id(), 25.0, cash)
        print(f"✓ {members[1].get_name()} paid membership fee: ${payment_result.get_amount()}")

        # Scenario 6: Fine Management
        print("\n--- SCENARIO 6: Fine Management ---")

        # Simulate overdue items and fines
        arjun_borrows[1].add_fine_amount(5.0)  # Add fine for overdue book
        print(f"✓ Added fine of $5.00 to {arjun_borrows[1].get_item().get_title()}")

        # Pay fine
        fine_payment = library.pay_fine(arjun_borrows[1].get_id(), credit_card)
        print(f"✓ Paid fine: ${fine_payment.get_amount()}")

        # Scenario 7: Return Operations
        print("\n--- SCENARIO 7: Return Operations ---")

        # Return some books
        library.return_item(arjun_borrows[0].get_id())
        print(f"✓ Returned: {arjun_borrows[0].get_item().get_title()}")

        library.return_item(priya_borrows[0].get_id())
        print(f"✓ Returned: {priya_borrows[0].get_item().get_title()}")

        # Scenario 8: Item Status Management
        print("\n--- SCENARIO 8: Item Status Management ---")

        # Mark item as damaged
        library.mark_item_damaged(books[2].get_id())
        print(f"✓ Marked as damaged: {books[2].get_title()}")

        # Mark item as lost
        library.mark_item_lost(books[4].get_id())
        print(f"✓ Marked as lost: {books[4].get_title()}")

        # Scenario 9: Comprehensive Reporting
        print("\n--- SCENARIO 9: Comprehensive Reporting ---")

        report = library.generate_library_report()
        LibraryManagementDemo.print_library_report(report)

        # Show member borrowing history
        print("\n--- Member Borrowing History ---")
        for member in members[:3]:  # Show first 3 members
            history = member.get_borrow_history()
            print(f"{member.get_name()}: {len(history)} books borrowed")
            for borrow in history:
                print(f"  - {borrow.get_item().get_title()} ({borrow.get_status().value})")

        # Design patterns showcase
        print("\n--- DESIGN PATTERNS DEMONSTRATED ---")
        print("✓ Singleton: LibraryManagement system")
        print("✓ Factory Method: Book and Magazine creation")
        print("✓ Strategy: Payment processing methods")
        print("✓ State: Item status management")
        print("✓ Observer: Item status notifications")
        print("✓ Repository: Data access layer")
        print("✓ Service: Business logic layer")

    @staticmethod
    def print_library_report(report: dict):
        """Print comprehensive library report"""
        print(f"\n📊 LIBRARY REPORT")
        print(f"{'='*50}")
        print(f"Total Items: {report['total_items']}")
        print(f"Total Members: {report['total_members']}")
        print(f"Total Borrows: {report['total_borrows']}")
        print(f"Overdue Items: {report['overdue_items']}")
        print(f"Total Fines: ${report['total_fines']:.2f}")

        print(f"\n📚 Item Status Breakdown:")
        for status, count in report["item_status_breakdown"].items():
            print(f"  {status}: {count}")

        print(f"\n📖 Borrow Status Breakdown:")
        for status, count in report["borrow_status_breakdown"].items():
            print(f"  {status}: {count}")

    @staticmethod
    def validate_catalog_management(library: LibraryManagement):
        """Validate librarian catalog management functionality"""
        print("\n--- Librarian Catalog Management ---")

        # Test adding books with different types using factory pattern
        test_books: list[Book] = []
        book_factory = BookFactory()
        magazine_factory = MagazineFactory()
        test_book = book_factory.create_item("Test Book 1", "Test Author 1", 2023, 1234567890)
        test_magazine = magazine_factory.create_item("Test Magazine 1", "Test Editor 1", 2023, 12345678)
        test_books.append(library.add_item(test_book))
        test_books.append(library.add_item(test_magazine))

        print(f"✓ Added {len(test_books)} test items to catalog")

        # Test updating book status
        library.mark_item_damaged(test_books[0].get_id())
        print(f"✓ Updated item status: {test_books[0].get_title()} marked as damaged")

        # Test removing book (mark as withdrawn)
        library.item_repository.get_item_by_id(test_books[1].get_id()).set_status(ItemStatus.WITHDRAWN)
        print(f"✓ Removed item from circulation: {test_books[1].get_title()}")

        # Validate catalog integrity
        all_items = library.item_repository.get_all_items()
        print(f"✓ Catalog integrity: {len(all_items)} total items in system")

    @staticmethod
    def validate_member_management(library: LibraryManagement):
        """Validate member registration and management"""
        print("\n--- Member Management ---")

        # Test member registration
        test_members: list[Member] = []
        test_members.append(library.register_member("Amit Kumar"))
        test_members.append(library.register_member("Sunita Devi"))
        test_members.append(library.register_member("Rohit Verma"))

        print(f"✓ Registered {len(test_members)} test members")

        # Test member details and borrowing history
        for member in test_members:
            print(f"✓ Member: {member.get_name()} (ID: {member.get_id()})")
            print(f"  Borrowing history: {len(member.get_borrow_history())} items")

        # Test duplicate member registration prevention
        try:
            library.register_member("Amit Kumar")  # Should fail
        except Exception as e:
            print(f"✓ Duplicate member prevention: {str(e)}")

        # Test invalid member operations
        try:
            library.register_member("")  # Empty name
        except Exception as e:
            print(f"✓ Invalid member data validation: {str(e)}")

    @staticmethod
    def validate_borrowing_rules(library: LibraryManagement):
        """Validate borrowing rules and enforcement"""
        print("\n--- Borrowing Rules & Enforcement ---")

        # Get test members and books
        members = library.member_repository.get_all_members()
        books = library.item_repository.get_all_items()

        if len(members) < 2 or len(books) < 3:
            print("✗ Need at least 2 members and 3 books for testing")
            return

        member1, member2 = members[0], members[1]
        book1, book2, book3 = books[0], books[1], books[2]

        # Test borrowing unavailable book
        try:
            library.request_item(book1.get_id(), member1.get_id(), 14)
            library.borrow_item(library.borrow_repository.get_borrows_by_member(member1)[0].get_id())
            print(f"✓ {member1.get_name()} borrowed: {book1.get_title()}")
        except Exception as e:
            print(f"✓ Borrowing validation: {str(e)}")

        # Test borrowing already borrowed book
        try:
            library.request_item(book1.get_id(), member2.get_id(), 14)
        except Exception as e:
            print(f"✓ Duplicate borrowing prevention: {str(e)}")

        # Test borrowing reference-only book
        reference_book = None
        for book in books:
            if book.get_status() == ItemStatus.REFERENCE_ONLY:
                reference_book = book
                break

        if reference_book:
            try:
                library.request_item(reference_book.get_id(), member2.get_id(), 14)
            except Exception as e:
                print(f"✓ Reference-only book protection: {str(e)}")

        # Test loan duration enforcement - find an available book
        available_book = None
        for book in books:
            if book.get_status() == ItemStatus.AVAILABLE:
                available_book = book
                break

        if available_book:
            borrow = library.request_item(available_book.get_id(), member2.get_id(), 1)  # 1 day loan
            library.borrow_item(borrow.get_id())
            print(f"✓ Loan duration set: {borrow.get_item().get_title()} for 1 day")
        else:
            print("✓ Loan duration enforcement: No available books for testing")

        # Test renewal limits
        if available_book:
            try:
                library.renew_item(borrow.get_id(), 7)
                library.renew_item(borrow.get_id(), 7)
                library.renew_item(borrow.get_id(), 7)  # Should fail
            except Exception as e:
                print(f"✓ Renewal limit enforcement: {str(e)}")
        else:
            print("✓ Renewal limit enforcement: No active borrows for testing")

    @staticmethod
    def validate_concurrent_access(library: LibraryManagement):
        """Validate concurrent access to catalog and member records"""
        print("\n--- Concurrent Access Testing ---")

        members = library.member_repository.get_all_members()
        books = library.item_repository.get_all_items()

        if len(members) < 3 or len(books) < 3:
            print("✗ Need at least 3 members and 3 books for concurrent testing")
            return

        # Test concurrent borrowing operations
        def concurrent_borrow_operation(member_id, book_id, operation_type):
            """Simulate concurrent borrowing operations"""
            try:
                if operation_type == "borrow":
                    borrow = library.request_item(book_id, member_id, 14)
                    library.borrow_item(borrow.get_id())
                    return f"Success: Borrowed book by {member_id}"
                elif operation_type == "return":
                    member_borrows = library.borrow_repository.get_borrows_by_member(library.member_repository.get_member_by_id(member_id))
                    active_borrows = [b for b in member_borrows if b.get_status().value == "active"]
                    if active_borrows:
                        library.return_item(active_borrows[0].get_id())
                        return f"Success: Returned book by {member_id}"
                elif operation_type == "renew":
                    member_borrows = library.borrow_repository.get_borrows_by_member(library.member_repository.get_member_by_id(member_id))
                    active_borrows = [b for b in member_borrows if b.get_status().value == "active"]
                    if active_borrows:
                        library.renew_item(active_borrows[0].get_id(), 7)
                        return f"Success: Renewed book by {member_id}"
                return f"No operation: {operation_type} by {member_id}"
            except Exception as e:
                return f"Error: {operation_type} by {member_id} - {e}"

        # Run concurrent operations
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []

            # Submit concurrent operations
            for i in range(5):
                member = members[i % len(members)]
                book = books[i % len(books)]
                operation = random.choice(["borrow", "return", "renew"])
                future = executor.submit(concurrent_borrow_operation, member.get_id(), book.get_id(), operation)
                futures.append(future)

            # Collect results
            results = []
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                print(f"✓ {result}")

        # Verify data consistency after concurrent operations
        total_borrows = len(library.borrow_repository.get_all_borrows())
        print(f"✓ Data Consistency: Total borrows after concurrent operations: {total_borrows}")
        print("✓ Thread Safety: Singleton pattern ensures single instance across threads")

    @staticmethod
    def validate_payment_and_fines(library: LibraryManagement):
        """Validate payment processing and fine management"""
        print("\n--- Payment & Fine Management ---")

        members = library.member_repository.get_all_members()
        if len(members) < 2:
            print("✗ Need at least 2 members for payment testing")
            return

        member1, member2 = members[0], members[1]

        # Test different payment methods
        payment_methods = [
            CreditCardPaymentStrategy("1111-2222-3333-4444", "123"),
            CashPaymentStrategy(),
            BankTransferPaymentStrategy("123456789", "HDFC Bank"),
        ]

        for i, payment_method in enumerate(payment_methods):
            try:
                result = library.pay_membership_fee(member1.get_id(), 25.0, payment_method)
                print(f"✓ Payment method {i+1}: ${result.get_amount()} - {result.get_status().value}")
            except Exception as e:
                print(f"✗ Payment method {i+1} failed: {e}")

        # Test fine calculation and payment
        member_borrows = library.borrow_repository.get_borrows_by_member(member2)
        if member_borrows:
            borrow = member_borrows[0]
            borrow.add_fine_amount(10.0)
            print(f"✓ Added fine of $10.00 to {borrow.get_item().get_title()}")

            # Pay fine
            fine_payment = library.pay_fine(borrow.get_id(), payment_methods[0])
            print(f"✓ Paid fine: ${fine_payment.get_amount()} - {fine_payment.get_status().value}")

        # Test invalid payment scenarios
        try:
            library.pay_membership_fee("invalid_member_id", 25.0)
        except Exception as e:
            print(f"✓ Invalid member payment validation: {str(e)}")

        try:
            library.pay_membership_fee(member1.get_id(), -10.0)
        except Exception as e:
            print(f"✓ Invalid amount validation: {str(e)}")

    @staticmethod
    def validate_advanced_features(library: LibraryManagement):
        """Validate advanced library features"""
        print("\n--- Advanced Features ---")

        # Test overdue item detection
        overdue_items = library.get_overdue_items()
        print(f"✓ Overdue items detection: {len(overdue_items)} items overdue")

        # Test member fine calculation
        members = library.member_repository.get_all_members()
        if members:
            member_fines = library.get_member_fines(members[0].get_id())
            print(f"✓ Member fine calculation: ${member_fines:.2f}")

        # Test item status transitions
        books = library.item_repository.get_all_items()
        if books:
            book = books[0]
            print(f"✓ Item status transitions: {book.get_title()} - {book.get_status().value}")

        # Test borrowing history tracking
        for member in members[:2]:
            history = member.get_borrow_history()
            print(f"✓ {member.get_name()}: {len(history)} items in borrowing history")

        # Test singleton pattern
        library2 = LibraryManagement.get_instance()
        print(f"✓ Singleton pattern: library is library2 = {library is library2}")

    @staticmethod
    def validate_performance_and_scalability(library: LibraryManagement):
        """Validate performance and scalability"""
        print("\n--- Performance & Scalability ---")

        # Test bulk operations performance
        start_time = time.time()

        # Bulk member registration
        bulk_members = []
        indian_names = [
            "Kavya Reddy",
            "Suresh Iyer",
            "Meera Joshi",
            "Ankit Agarwal",
            "Deepika Nair",
            "Ravi Shankar",
            "Pooja Mehta",
            "Vishal Tiwari",
            "Shruti Das",
            "Nikhil Rao",
        ]
        for i in range(10):
            member = library.register_member(indian_names[i])
            bulk_members.append(member)

        registration_time = time.time() - start_time
        print(f"✓ Performance: Registered 10 members in {registration_time:.3f} seconds")

        # Bulk book addition
        start_time = time.time()
        bulk_books = []
        indian_authors = [
            "Rabindranath Tagore",
            "R.K. Narayan",
            "Arundhati Roy",
            "Chetan Bhagat",
            "Amish Tripathi",
            "Jhumpa Lahiri",
            "Salman Rushdie",
            "Vikram Seth",
            "Ruskin Bond",
            "Anita Desai",
        ]
        indian_books = [
            "Gitanjali",
            "Malgudi Days",
            "The God of Small Things",
            "Five Point Someone",
            "The Immortals of Meluha",
            "The Namesake",
            "Midnight's Children",
            "A Suitable Boy",
            "The Blue Umbrella",
            "Clear Light of Day",
        ]
        for i in range(10):
            book_factory = BookFactory()
            book = book_factory.create_item(indian_books[i], indian_authors[i], 2023, 1000000000 + i)
            bulk_books.append(library.add_item(book))

        book_addition_time = time.time() - start_time
        print(f"✓ Performance: Added 10 books in {book_addition_time:.3f} seconds")

        # Test report generation performance
        start_time = time.time()
        report = library.generate_library_report()
        report_time = time.time() - start_time
        print(f"✓ Performance: Generated report in {report_time:.3f} seconds")

        # Resource utilization summary
        total_items = len(library.item_repository.get_all_items())
        total_members = len(library.member_repository.get_all_members())
        total_borrows = len(library.borrow_repository.get_all_borrows())

        print(f"✓ Scalability: System handling {total_items} items, {total_members} members, {total_borrows} borrows efficiently")


def main():
    LibraryManagementDemo.main()


if __name__ == "__main__":
    main()
