"""
Online Auction System Demo

Comprehensive demonstration of the online auction system showcasing:
- User registration and management
- Auction creation and management
- Bidding workflow with design patterns
- Chain of Responsibility for validation
- Mediator pattern for coordination
- Command pattern for operations
- State pattern for auction lifecycle
- Strategy pattern for different auction types
- Observer pattern for notifications

Author: Amit Kumar
"""

from datetime import datetime, timedelta
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.models.user import User
from app.models.auction_item import AuctionItem
from app.models.auction import EnglishAuction, DutchAuction, SealedBidAuction
from app.models.bid import Bid
from app.models.enums import AuctionItemType, AuctionStatus
from app.mediator.auction_mediator import ConcreteAuctionMediator
from app.commands.auction_command import PlaceBidCommand


def concurrent_bidding_test(mediator: ConcreteAuctionMediator, auction, num_users: int = 5):
    """Test concurrent bidding using ThreadPoolExecutor"""
    print(f"🚀 Testing {num_users} concurrent bidders on auction {auction.get_id()[:8]}...")

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

    # Execute concurrent bids using ThreadPoolExecutor
    start_time = time.time()

    # Create bids with different amounts
    bid_amounts = [1200.0, 1500.0, 1800.0, 2000.0, 2200.0]

    with ThreadPoolExecutor(max_workers=num_users) as executor:
        # Submit all bidding tasks
        future_to_user = {executor.submit(attempt_bid, user, bid_amounts[i]): user for i, user in enumerate(concurrent_users)}

        # Collect results as they complete
        for future in as_completed(future_to_user):
            result = future.result()
            results["bid_details"].append(result)

            if result["success"]:
                results["successful_bids"] += 1
            else:
                results["failed_bids"] += 1

    end_time = time.time()
    execution_time = end_time - start_time

    # Print results summary
    print(f"📊 Results: {results['successful_bids']}/{num_users} successful bids ({execution_time:.2f}s)")

    return results


def main():
    print("=== ONLINE AUCTION SYSTEM DEMO ===\n")

    # ==================== MEDIATOR SETUP ====================
    print("1. INITIALIZING SYSTEM")
    print("-" * 30)

    # Create the central mediator
    mediator = ConcreteAuctionMediator()
    print("✅ Mediator initialized with Chain of Responsibility")
    print("   - RateLimitHandler: 5 requests/minute per user")
    print("   - ValidationHandler: Bid validation")
    print()

    # ==================== USER REGISTRATION ====================
    print("2. USER REGISTRATION")
    print("-" * 25)

    # Create users
    arjun = User("Arjun Sharma", "arjun.sharma@email.com", "password123")
    priya = User("Priya Patel", "priya.patel@email.com", "password123")
    rahul = User("Rahul Singh", "rahul.singh@email.com", "password123")
    sneha = User("Sneha Gupta", "sneha.gupta@email.com", "password123")
    vikram = User("Vikram Kumar", "vikram.kumar@email.com", "password123")

    # Register users with mediator
    users = [arjun, priya, rahul, sneha, vikram]
    for user in users:
        mediator.register_component(user)

    print(f"✅ Registered {len(users)} users:")
    for user in users:
        print(f"   - {user.get_name()} ({user.get_email()})")
    print()

    # ==================== AUCTION CREATION ====================
    print("3. AUCTION CREATION")
    print("-" * 25)

    # Create auction items
    guitar_item = AuctionItem(
        name="Vintage Gibson Guitar",
        description="Beautiful vintage acoustic guitar from 1970s",
        starting_price=1000.0,
        item_type=AuctionItemType.PHYSICAL,
    )

    painting_item = AuctionItem(
        name="Modern Art Painting",
        description="Contemporary abstract painting by local artist",
        starting_price=2000.0,
        item_type=AuctionItemType.PHYSICAL,
    )

    software_item = AuctionItem(
        name="Premium Software License",
        description="Lifetime license for professional design software",
        starting_price=500.0,
        item_type=AuctionItemType.DIGITAL,
    )

    # Create different types of auctions
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=10)

    # English Auction (ascending bids)
    guitar_auction = EnglishAuction(owner=arjun, item=guitar_item, start_time=start_time, end_time=end_time, starting_price=1000.0)

    # Dutch Auction (descending bids)
    painting_auction = DutchAuction(
        owner=priya, item=painting_item, start_time=start_time + timedelta(minutes=2), end_time=end_time + timedelta(minutes=2), starting_price=2000.0
    )

    # Sealed Bid Auction
    software_auction = SealedBidAuction(
        owner=rahul, item=software_item, start_time=start_time + timedelta(minutes=4), end_time=end_time + timedelta(minutes=4), starting_price=500.0
    )

    # Register auctions with mediator
    auctions = [guitar_auction, painting_auction, software_auction]
    for auction in auctions:
        mediator.register_component(auction)

    print(f"✅ Created {len(auctions)} auctions:")
    print(f"   - {guitar_item.get_name()} (English Auction) - Starting: ₹{guitar_auction.get_starting_price()}")
    print(f"   - {painting_item.get_name()} (Dutch Auction) - Starting: ₹{painting_auction.get_starting_price()}")
    print(f"   - {software_item.get_name()} (Sealed Bid Auction) - Starting: ₹{software_auction.get_starting_price()}")
    print()

    # ==================== AUCTION STATE MANAGEMENT ====================
    print("4. AUCTION STATE MANAGEMENT")
    print("-" * 35)

    # Start auctions using direct method calls
    print("🚀 Starting auctions:")
    guitar_auction.start_auction()
    print(f"   - Guitar auction status: {guitar_auction.get_status().value}")

    painting_auction.start_auction()
    print(f"   - Painting auction status: {painting_auction.get_status().value}")

    software_auction.start_auction()
    print(f"   - Software auction status: {software_auction.get_status().value}")
    print()

    # ==================== BIDDING WORKFLOW ====================
    print("5. BIDDING WORKFLOW")
    print("-" * 25)

    # English Auction Bidding (ascending)
    print("📈 English Auction Bidding (Ascending):")
    guitar_bids = [(priya, 1200.0), (rahul, 1500.0), (sneha, 1800.0), (vikram, 2000.0), (priya, 2200.0)]  # Priya outbids herself

    for user, amount in guitar_bids:
        bid = Bid(user, guitar_auction, amount)
        command = PlaceBidCommand(bid)

        print(f"   {user.get_name()} bidding ₹{amount}...")
        success = command.execute()

        if success:
            print(f"   ✅ Bid accepted! Current price: ₹{guitar_auction.get_current_price()}")
        else:
            print(f"   ❌ Bid rejected!")
        print()

    # Dutch Auction Bidding (descending)
    print("📉 Dutch Auction Bidding (Descending):")
    painting_bids = [(rahul, 1800.0), (sneha, 1500.0), (vikram, 1200.0)]

    for user, amount in painting_bids:
        bid = Bid(user, painting_auction, amount)
        command = PlaceBidCommand(bid)

        print(f"   {user.get_name()} bidding ₹{amount}...")
        success = command.execute()

        if success:
            print(f"   ✅ Bid accepted! Current price: ₹{painting_auction.get_current_price()}")
        else:
            print(f"   ❌ Bid rejected!")
        print()

    # Sealed Bid Auction
    print("🔒 Sealed Bid Auction:")
    sealed_bids = [(arjun, 600.0), (priya, 750.0), (sneha, 800.0), (vikram, 900.0)]

    for user, amount in sealed_bids:
        bid = Bid(user, software_auction, amount)
        command = PlaceBidCommand(bid)

        print(f"   {user.get_name()} placing sealed bid ₹{amount}...")
        success = command.execute()

        if success:
            print(f"   ✅ Sealed bid placed!")
        else:
            print(f"   ❌ Bid rejected!")
        print()

    # ==================== RATE LIMITING DEMO ====================
    print("6. RATE LIMITING DEMO")
    print("-" * 25)

    print("🚫 Testing rate limiting (5 requests/minute per user):")

    # Try to exceed rate limit
    for i in range(7):  # Exceed the 5 request limit
        bid = Bid(arjun, guitar_auction, 2500.0 + i * 100)
        command = PlaceBidCommand(bid)

        print(f"   Attempt {i+1}: Arjun bidding ₹{2500.0 + i * 100}...")
        success = command.execute()

        if not success:
            print(f"   ❌ Rate limit exceeded after {i+1} attempts!")
            break
        else:
            print(f"   ✅ Bid {i+1} accepted")
    print()

    # ==================== BID REMOVAL DEMO ====================
    print("7. BID REMOVAL DEMO")
    print("-" * 25)

    print("🗑️ Testing bid removal and price updates:")

    # Show current state before removal
    print(f"   Current bids: {len(guitar_auction.get_bids())}")
    print(f"   Current price: ₹{guitar_auction.get_current_price()}")

    # Get the latest bid from guitar auction
    guitar_bids_list = guitar_auction.get_bids()
    if guitar_bids_list:
        latest_bid = guitar_bids_list[-1]
        print(f"   Removing {latest_bid.get_user().get_name()}'s bid of ₹{latest_bid.get_amount()}")

        success = guitar_auction.remove_bid(latest_bid)

        if success:
            print(f"   ✅ Bid removed! New current price: ₹{guitar_auction.get_current_price()}")
            print(f"   Remaining bids: {len(guitar_auction.get_bids())}")
        else:
            print(f"   ❌ Bid removal failed!")
    print()

    # ==================== DUTCH AUCTION TEST ====================
    print("8. DUTCH AUCTION TEST")
    print("-" * 25)

    print("📉 Testing Dutch Auction (Descending Price):")
    print(f"   Starting price: ₹{painting_auction.get_starting_price()}")
    print(f"   Current price: ₹{painting_auction.get_current_price()}")

    # Test Dutch auction with descending bids
    dutch_bids = [
        (rahul, 1900.0),  # Below starting price
        (sneha, 1500.0),  # Further below
        (vikram, 1200.0),  # Even lower
        (arjun, 1000.0),  # Lowest bid
    ]

    print("   Placing descending bids on Dutch auction:")
    for user, amount in dutch_bids:
        bid = Bid(user, painting_auction, amount)
        command = PlaceBidCommand(bid)

        print(f"   {user.get_name()} bidding ₹{amount}...")
        success = command.execute()

        if success:
            print(f"   ✅ Bid accepted! Current price: ₹{painting_auction.get_current_price()}")
        else:
            print(f"   ❌ Bid rejected!")
        print()

    # Show final Dutch auction state
    print(f"   Dutch auction final state:")
    print(f"   - Total bids: {len(painting_auction.get_bids())}")
    print(f"   - Current price: ₹{painting_auction.get_current_price()}")
    print(f"   - Winner: {painting_auction.determine_winner().get_name() if painting_auction.determine_winner() else 'None'}")
    print()

    # ==================== CONCURRENT BIDDING TEST ====================
    print("9. CONCURRENT BIDDING TEST")
    print("-" * 35)

    # Test concurrent bidding on guitar auction
    concurrent_bidding_test(mediator, guitar_auction, num_users=5)
    print()

    # ==================== AUCTION ENDING ====================
    print("10. AUCTION ENDING")
    print("-" * 20)

    print("🏁 Ending auctions:")

    # End auctions
    guitar_auction.end_auction()
    guitar_winner = guitar_auction.determine_winner()
    print(f"   - Guitar auction ended. Winner: {guitar_winner.get_name() if guitar_winner else 'None'}")
    print(f"     Final price: ₹{guitar_auction.get_current_price()}")
    print(f"     Status: {guitar_auction.get_status().value}")

    painting_auction.end_auction()
    painting_winner = painting_auction.determine_winner()
    print(f"   - Painting auction ended. Winner: {painting_winner.get_name() if painting_winner else 'None'}")
    print(f"     Final price: ₹{painting_auction.get_current_price()}")
    print(f"     Status: {painting_auction.get_status().value}")

    software_auction.end_auction()
    software_winner = software_auction.determine_winner()
    print(f"   - Software auction ended. Winner: {software_winner.get_name() if software_winner else 'None'}")
    print(f"     Final price: ₹{software_auction.get_current_price()}")
    print(f"     Status: {software_auction.get_status().value}")
    print()

    # ==================== AUCTION STATISTICS ====================
    print("11. AUCTION STATISTICS")
    print("-" * 30)

    print("📊 System Overview:")
    print(f"   Total Users: {len(users)}")
    print(f"   Total Auctions: {len(auctions)}")
    print(f"   Active Auctions: {len([a for a in auctions if a.get_status() == AuctionStatus.ACTIVE])}")
    print(f"   Closed Auctions: {len([a for a in auctions if a.get_status() == AuctionStatus.CLOSED])}")

    total_bids = sum(len(auction.get_bids()) for auction in auctions)
    print(f"   Total Bids Placed: {total_bids}")

    total_revenue = sum(auction.get_current_price() for auction in auctions)
    print(f"   Total Revenue: ₹{total_revenue:.2f}")
    print()

    # ==================== USER BIDDING HISTORY ====================
    print("12. USER BIDDING HISTORY")
    print("-" * 30)

    for user in users:
        history = user.get_bidding_history()
        if history:
            print(f"   {user.get_name()}: {len(history)} bids")
            for bid in history:
                print(f"     - ₹{bid.get_amount()} on {bid.get_auction().get_item().get_name()}")
        else:
            print(f"   {user.get_name()}: No bids placed")
    print()

    # ==================== DESIGN PATTERNS SUMMARY ====================
    print("13. DESIGN PATTERNS DEMONSTRATED")
    print("-" * 40)

    print("🎯 Design Patterns Used:")
    print("   ✅ Mediator Pattern: Centralized coordination between components")
    print("   ✅ Chain of Responsibility: Rate limiting and validation")
    print("   ✅ Command Pattern: Encapsulated operations with undo capability")
    print("   ✅ State Pattern: Auction lifecycle management")
    print("   ✅ Strategy Pattern: Different auction types (English, Dutch, Sealed)")
    print("   ✅ Observer Pattern: Notification system for auction updates")
    print("   ✅ Component Pattern: Reusable base for all mediator participants")
    print()

    # ==================== SYSTEM FEATURES ====================
    print("14. SYSTEM FEATURES")
    print("-" * 25)

    print("🚀 Key Features Demonstrated:")
    print("   ✅ User Registration and Management")
    print("   ✅ Multiple Auction Types (English, Dutch, Sealed Bid)")
    print("   ✅ Real-time Bidding with Validation")
    print("   ✅ Rate Limiting (5 requests/minute per user)")
    print("   ✅ Concurrent Access Handling")
    print("   ✅ Bid Placement and Removal")
    print("   ✅ Automatic Winner Determination")
    print("   ✅ Auction State Management")
    print("   ✅ Extensible Architecture")
    print()

    print("=== DEMO COMPLETED ===")
    print("\n💡 Note: In production, auctions would be ended automatically")
    print("   by cron jobs based on their end_time, not manually.")


if __name__ == "__main__":
    main()
