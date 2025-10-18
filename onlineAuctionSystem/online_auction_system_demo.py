from datetime import datetime, timedelta
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.models.user import User
from app.models.auction_item import AuctionItem
from app.models.auction import EnglishAuction, DutchAuction, SealedBidAuction
from app.models.bid import Bid
from app.models.enums import AuctionItemType, AuctionStatus, PaymentMethod
from app.mediator.auction_mediator import ConcreteAuctionMediator
from app.commands.auction_command import PlaceBidCommand
from app.services.payment_service import PaymentService
from app.strategies.payment_strategies import CreditCardPaymentStrategy, DebitCardPaymentStrategy, CashPaymentStrategy
from app.services.search_service import SearchService
from app.strategies.search_strategy import (
    AuctionItemTitleSearchStrategy,
    AuctionItemStartingPriceSearchStrategy,
    AuctionItemStartingPriceRangeSearchStrategy,
    AuctionStatusSearchStrategy,
)
from app.repositories.auction_repository import AuctionRepository


def concurrent_bidding_test(mediator: ConcreteAuctionMediator, auction, num_users: int = 5):
    """Test concurrent bidding using ThreadPoolExecutor"""
    print(f"🚀 Testing {num_users} concurrent bidders...")

    # Create users for concurrent bidding
    concurrent_users = []
    for i in range(num_users):
        user = User(f"Concurrent Bidder {i+1}", f"bidder{i+1}@concurrent.com", "password123")
        mediator.register_component(user)
        concurrent_users.append(user)

    # Results tracking
    results = {"successful_bids": 0, "failed_bids": 0, "bid_details": []}

    def attempt_bid(user: User, bid_amount: float):
        """Function to be executed by each thread"""
        thread_id = threading.current_thread().ident
        try:
            bid = Bid(user, auction, bid_amount)
            command = PlaceBidCommand(bid)
            success = command.execute()

            if success:
                return {
                    "success": True,
                    "user": user.get_name(),
                    "amount": bid_amount,
                    "thread_id": thread_id,
                }
            else:
                return {"success": False, "user": user.get_name(), "amount": bid_amount, "reason": "Bid rejected", "thread_id": thread_id}

        except Exception as e:
            return {"success": False, "user": user.get_name(), "amount": bid_amount, "reason": str(e), "thread_id": thread_id}

    # Execute concurrent bids
    with ThreadPoolExecutor(max_workers=num_users) as executor:
        # Submit all bid attempts
        future_to_user = {executor.submit(attempt_bid, user, 1000.0 + (i * 100)): user for i, user in enumerate(concurrent_users)}

        # Collect results
        for future in as_completed(future_to_user):
            result = future.result()
            results["bid_details"].append(result)

            if result["success"]:
                results["successful_bids"] += 1
            else:
                results["failed_bids"] += 1

    # Print results
    print(f"   ✅ Successful bids: {results['successful_bids']}")
    print(f"   ❌ Failed bids: {results['failed_bids']}")
    print(f"   💰 Final price: ₹{auction.get_current_price()}")
    print(f"   👑 Winner: {auction.determine_winner().get_name() if auction.determine_winner() else 'None'}")


def main():
    print("🏛️ ONLINE AUCTION SYSTEM DEMO")
    print("=" * 50)

    # Initialize system
    mediator = ConcreteAuctionMediator()
    print("✅ System initialized")

    # Create users
    arjun = User("Arjun Sharma", "arjun.sharma@email.com", "password123")
    priya = User("Priya Patel", "priya.patel@email.com", "password123")
    rahul = User("Rahul Singh", "rahul.singh@email.com", "password123")
    sneha = User("Sneha Gupta", "sneha.gupta@email.com", "password123")
    vikram = User("Vikram Kumar", "vikram.kumar@email.com", "password123")

    users = [arjun, priya, rahul, sneha, vikram]
    for user in users:
        mediator.register_component(user)

    print(f"✅ Registered {len(users)} users")

    # Create auction items
    guitar_item = AuctionItem("Vintage Guitar", "Beautiful vintage guitar from 1960s", 1000.0, AuctionItemType.PHYSICAL)
    painting_item = AuctionItem("Abstract Painting", "Modern abstract art piece", 2000.0, AuctionItemType.PHYSICAL)
    software_item = AuctionItem("Software License", "Premium software license for 1 year", 500.0, AuctionItemType.DIGITAL)

    # Create auctions
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=10)

    guitar_auction = EnglishAuction(owner=arjun, item=guitar_item, start_time=start_time, end_time=end_time, starting_price=1000.0)
    painting_auction = DutchAuction(
        owner=priya, item=painting_item, start_time=start_time + timedelta(minutes=2), end_time=end_time + timedelta(minutes=2), starting_price=2000.0
    )
    software_auction = SealedBidAuction(
        owner=rahul, item=software_item, start_time=start_time + timedelta(minutes=4), end_time=end_time + timedelta(minutes=4), starting_price=500.0
    )

    auctions = [guitar_auction, painting_auction, software_auction]
    for auction in auctions:
        mediator.register_component(auction)

    # Add to repository for search
    auction_repository = AuctionRepository()
    for auction in auctions:
        auction_repository.add_auction(auction)

    print(f"✅ Created {len(auctions)} auctions")

    # Start auctions
    guitar_auction.start_auction()
    painting_auction.start_auction()
    software_auction.start_auction()
    print("✅ All auctions started")

    # Bidding workflow
    print("\n📈 BIDDING WORKFLOW")
    print("-" * 20)

    # English Auction Bidding
    print("English Auction Bidding:")
    guitar_bids = [(priya, 1200.0), (rahul, 1500.0), (sneha, 1800.0), (vikram, 2000.0), (priya, 2200.0)]

    for user, amount in guitar_bids:
        bid = Bid(user, guitar_auction, amount)
        command = PlaceBidCommand(bid)
        success = command.execute()
        if success:
            print(f"   ✅ {user.get_name()} bid ₹{amount}")

    print(f"   Final price: ₹{guitar_auction.get_current_price()}")
    print(f"   Winner: {guitar_auction.determine_winner().get_name() if guitar_auction.determine_winner() else 'None'}")

    # Dutch Auction Bidding
    print("\nDutch Auction Bidding:")
    dutch_bids = [(rahul, 2000.0), (sneha, 1800.0), (vikram, 1500.0), (arjun, 1200.0)]

    for user, amount in dutch_bids:
        bid = Bid(user, painting_auction, amount)
        command = PlaceBidCommand(bid)
        success = command.execute()
        if success:
            print(f"   ✅ {user.get_name()} bid ₹{amount}")

    print(f"   Final price: ₹{painting_auction.get_current_price()}")
    print(f"   Winner: {painting_auction.determine_winner().get_name() if painting_auction.determine_winner() else 'None'}")

    # Sealed Bid Auction
    print("\nSealed Bid Auction:")
    sealed_bids = [(sneha, 600.0), (vikram, 700.0), (priya, 550.0)]

    for user, amount in sealed_bids:
        bid = Bid(user, software_auction, amount)
        command = PlaceBidCommand(bid)
        success = command.execute()
        if success:
            print(f"   ✅ {user.get_name()} bid ₹{amount}")

    print(f"   Final price: ₹{software_auction.get_current_price()}")
    print(f"   Winner: {software_auction.determine_winner().get_name() if software_auction.determine_winner() else 'None'}")

    # Bid removal test
    print("\n🗑️ BID REMOVAL TEST")
    print("-" * 20)
    guitar_bids_list = guitar_auction.get_bids()
    if guitar_bids_list:
        latest_bid = guitar_bids_list[-1]
        print(f"Removing bid: ₹{latest_bid.get_amount()} by {latest_bid.get_user().get_name()}")
        success = guitar_auction.remove_bid(latest_bid)
        if success:
            print(f"   ✅ Bid removed! New price: ₹{guitar_auction.get_current_price()}")

    # Search functionality
    print("\n🔍 SEARCH FUNCTIONALITY")
    print("-" * 20)

    search_service = SearchService()

    # Search by title
    print("Search by title 'guitar':")
    title_search_strategy = AuctionItemTitleSearchStrategy()
    search_service.set_search_strategy(title_search_strategy)
    results = search_service.search("guitar")
    print(f"   Found {len(results)} auction(s)")

    # Search by price range
    print("Search by price range ₹500-₹1500:")
    price_range_strategy = AuctionItemStartingPriceRangeSearchStrategy()
    search_service.set_search_strategy(price_range_strategy)
    results = search_service.search((500, 1500))
    print(f"   Found {len(results)} auction(s)")

    # Payment processing
    print("\n💳 PAYMENT PROCESSING")
    print("-" * 20)

    payment_amounts = [500.0, 1200.0, 2500.0]

    # Credit Card Payment
    print("Credit Card Payment:")
    credit_card_strategy = CreditCardPaymentStrategy("1234-5678-9012-3456", "12/25", "123")
    credit_payment_service = PaymentService(credit_card_strategy)

    for amount in payment_amounts:
        response = credit_payment_service.process_payment(amount)
        print(f"   Amount: ₹{amount} | Status: {response.get_status().value}")

    # Debit Card Payment
    print("\nDebit Card Payment:")
    debit_card_strategy = DebitCardPaymentStrategy("9876-5432-1098-7654", "06/26", "456")
    debit_payment_service = PaymentService(debit_card_strategy)

    for amount in payment_amounts:
        response = debit_payment_service.process_payment(amount)
        print(f"   Amount: ₹{amount} | Status: {response.get_status().value}")

    # Cash Payment
    print("\nCash Payment:")
    cash_strategy = CashPaymentStrategy()
    cash_payment_service = PaymentService(cash_strategy)

    for amount in payment_amounts:
        response = cash_payment_service.process_payment(amount)
        print(f"   Amount: ₹{amount} | Status: {response.get_status().value}")

    # Concurrent bidding test
    print("\n🚀 CONCURRENT BIDDING TEST")
    print("-" * 25)
    concurrent_bidding_test(mediator, guitar_auction, num_users=5)

    # End auctions and determine winners
    print("\n🏁 AUCTION RESULTS")
    print("-" * 20)

    guitar_auction.end_auction()
    painting_auction.end_auction()
    software_auction.end_auction()

    print(
        f"Guitar Auction - Winner: {guitar_auction.determine_winner().get_name() if guitar_auction.determine_winner() else 'None'} | Price: ₹{guitar_auction.get_current_price()}"
    )
    print(
        f"Painting Auction - Winner: {painting_auction.determine_winner().get_name() if painting_auction.determine_winner() else 'None'} | Price: ₹{painting_auction.get_current_price()}"
    )
    print(
        f"Software Auction - Winner: {software_auction.determine_winner().get_name() if software_auction.determine_winner() else 'None'} | Price: ₹{software_auction.get_current_price()}"
    )

    print("\n✅ DEMO COMPLETED")
    print("All requirements demonstrated successfully!")


if __name__ == "__main__":
    main()
