from ride_sharing_system import RideSharingSystem
from app.models.location import Location
from app.models.enums import RideType, DriverStatus
from app.models.vehicle_factory import AutoFactory, SedanFactory, SUVFactory, LuxuryFactory
from app.strategies.driver_matching_strategy import NearestDriverMatchingStrategy
from app.strategies.pricing_strategy import VehicleBasedPricingStrategy, DistanceBasedPricingStrategy
from app.decorators.pricing_decorator import DiscountDecorator, SurgeDecorator, TaxDecorator


class RideSharingSystemDemo:
    @staticmethod
    def run():
        print("🚗 Ride Sharing System Demo - Design Patterns Showcase")
        print("=" * 60)

        # Singleton Pattern - Get system instance
        system = RideSharingSystem.get_instance()

        # Strategy Pattern - Set driver matching and pricing strategies
        system.set_driver_matching_strategy(NearestDriverMatchingStrategy(max_distance=10.0))

        # Factory Pattern - Create vehicles using vehicle factories
        auto_factory = AutoFactory()
        sedan_factory = SedanFactory()
        suv_factory = SUVFactory()
        luxury_factory = LuxuryFactory()

        # Register riders
        alice = system.register_rider("Alice", "123-456-7890")
        bob = system.register_rider("Bob", "987-654-3210")

        # Register drivers with different vehicle types using Factory Pattern
        driver1 = system.register_driver("John", "111-222-3333", auto_factory.create_vehicle("KA01-1234", "Bajaj Auto"), Location(1.0, 1.0))

        driver2 = system.register_driver("Sarah", "444-555-6666", sedan_factory.create_vehicle("KA02-5678", "Toyota Camry"), Location(2.0, 2.0))

        driver3 = system.register_driver("Mike", "777-888-9999", suv_factory.create_vehicle("KA03-9012", "Honda CRV"), Location(3.0, 3.0))

        driver4 = system.register_driver("Emma", "000-111-2222", luxury_factory.create_vehicle("KA04-3456", "Mercedes S-Class"), Location(5.0, 5.0))

        # Set drivers online
        for driver in [driver1, driver2, driver3, driver4]:
            driver.set_status(DriverStatus.AVAILABLE)

        print(f"\n✅ Registered {len([alice, bob])} riders and {len([driver1, driver2, driver3, driver4])} drivers")

        # Demo 1: Basic ride with different pricing strategies
        print("\n📋 Demo 1: Basic Ride with Vehicle-Based Pricing")
        print("-" * 50)

        base_pricing = VehicleBasedPricingStrategy(base_fare=10.0)
        ride1 = system.request_ride(alice.get_id(), Location(0.0, 0.0), Location(5.0, 5.0), RideType.SEDAN, base_pricing)

        if ride1:
            print(f"💰 Base fare: ₹{ride1.get_fare():.2f}")
            system.accept_ride(driver2.get_id(), ride1)
            system.start_ride(ride1.get_id())
            system.complete_ride(ride1.get_id())
            # Add earnings to driver (assuming 80% goes to driver, 20% to platform)
            driver2.add_earnings(ride1.get_fare() * 0.8)

        # Demo 2: Decorator Pattern - Pricing with discounts and surge
        print("\n📋 Demo 2: Decorator Pattern - Pricing with Discount & Surge")
        print("-" * 50)

        # Create pricing decorators
        distance_pricing = DistanceBasedPricingStrategy(base_fare=5.0, rate_per_km=8.0)
        discount_pricing = DiscountDecorator(distance_pricing, 0.1)  # 10% discount
        surge_pricing = SurgeDecorator(discount_pricing, 1.5)  # 1.5x surge
        final_pricing = TaxDecorator(surge_pricing, 0.18)  # 18% tax

        ride2 = system.request_ride(bob.get_id(), Location(1.0, 1.0), Location(8.0, 8.0), RideType.SUV, final_pricing)

        if ride2:
            print(f"💰 Final fare with decorators: ₹{ride2.get_fare():.2f}")
            system.accept_ride(driver3.get_id(), ride2)
            system.start_ride(ride2.get_id())
            system.complete_ride(ride2.get_id())
            # Add earnings to driver
            driver3.add_earnings(ride2.get_fare() * 0.8)

        # Demo 3: Different vehicle types and matching strategy
        print("\n📋 Demo 3: Different Vehicle Types & Matching Strategy")
        print("-" * 50)

        # Request luxury ride
        ride3 = system.request_ride(alice.get_id(), Location(2.0, 2.0), Location(10.0, 10.0), RideType.LUXURY, base_pricing)

        if ride3:
            print(f"💰 Luxury ride fare: ₹{ride3.get_fare():.2f}")
            system.accept_ride(driver4.get_id(), ride3)
            system.start_ride(ride3.get_id())
            system.complete_ride(ride3.get_id())
            # Add earnings to driver
            driver4.add_earnings(ride3.get_fare() * 0.8)

        # Demo 4: Observer Pattern - Ride status notifications
        print("\n📋 Demo 4: Observer Pattern - Ride Status Notifications")
        print("-" * 50)

        ride4 = system.request_ride(bob.get_id(), Location(0.5, 0.5), Location(3.0, 3.0), RideType.AUTO, base_pricing)

        if ride4:
            print(f"💰 Auto ride fare: ₹{ride4.get_fare():.2f}")
            system.accept_ride(driver1.get_id(), ride4)
            system.start_ride(ride4.get_id())
            system.complete_ride(ride4.get_id())
            # Add earnings to driver
            driver1.add_earnings(ride4.get_fare() * 0.8)

        # Demo 5: State Pattern - Ride state transitions
        print("\n📋 Demo 5: State Pattern - Ride State Transitions")
        print("-" * 50)

        ride5 = system.request_ride(alice.get_id(), Location(1.5, 1.5), Location(4.0, 4.0), RideType.SEDAN, base_pricing)

        if ride5:
            print(f"💰 Sedan ride fare: ₹{ride5.get_fare():.2f}")
            print(f"📊 Ride state: {ride5.get_status().value}")

            system.accept_ride(driver2.get_id(), ride5)
            print(f"📊 Ride state: {ride5.get_status().value}")

            system.start_ride(ride5.get_id())
            print(f"📊 Ride state: {ride5.get_status().value}")

            system.complete_ride(ride5.get_id())
            print(f"📊 Ride state: {ride5.get_status().value}")
            # Add earnings to driver
            driver2.add_earnings(ride5.get_fare() * 0.8)

        # Demo 6: Edge Cases - No Available Drivers
        print("\n📋 Demo 6: Edge Cases - No Available Drivers")
        print("-" * 50)

        # Set all drivers to BUSY status
        print("Setting all drivers to BUSY status...")
        for driver in [driver1, driver2, driver3, driver4]:
            driver.set_status(DriverStatus.BUSY)

        # Try to request a ride when no drivers are available
        ride6 = system.request_ride(alice.get_id(), Location(1.0, 1.0), Location(3.0, 3.0), RideType.SEDAN, base_pricing)

        if ride6 is None:
            print("❌ Ride request failed: No available drivers found!")
            print("💡 This demonstrates the system's ability to handle driver unavailability")

        # Demo 7: Ride Cancellation Scenario
        print("\n📋 Demo 7: Ride Cancellation Scenario")
        print("-" * 50)

        # Set one driver back to available
        driver2.set_status(DriverStatus.AVAILABLE)

        # Request a ride
        ride7 = system.request_ride(bob.get_id(), Location(2.0, 2.0), Location(4.0, 4.0), RideType.SEDAN, base_pricing)

        if ride7:
            print(f"💰 Ride fare: ₹{ride7.get_fare():.2f}")
            print(f"📊 Ride state: {ride7.get_status().value}")

            # Accept the ride
            system.accept_ride(driver2.get_id(), ride7)
            print(f"📊 Ride state: {ride7.get_status().value}")

            # Cancel the ride before starting
            print("🚫 Rider decides to cancel the ride...")
            system.cancel_ride(ride7.get_id(), bob)
            print(f"📊 Ride state: {ride7.get_status().value}")
            print("💡 This demonstrates ride cancellation handling")

        # Demo 8: Driver Goes Offline During Ride
        print("\n📋 Demo 8: Driver Goes Offline During Ride")
        print("-" * 50)

        # Set another driver available
        driver3.set_status(DriverStatus.AVAILABLE)

        # Request a ride
        ride8 = system.request_ride(alice.get_id(), Location(1.5, 1.5), Location(3.5, 3.5), RideType.SUV, base_pricing)

        if ride8:
            print(f"💰 Ride fare: ₹{ride8.get_fare():.2f}")

            # Accept and start the ride
            system.accept_ride(driver3.get_id(), ride8)
            system.start_ride(ride8.get_id())
            print(f"📊 Ride state: {ride8.get_status().value}")

            # Driver goes offline (simulating phone battery death, network issues, etc.)
            print("📱 Driver's phone goes offline (battery dead)...")
            driver3.set_status(DriverStatus.OFFLINE)
            print(f"🚗 Driver {driver3.get_name()} is now OFFLINE")

            # Complete the ride anyway (driver might have completed it before going offline)
            system.complete_ride(ride8.get_id())
            print(f"📊 Ride state: {ride8.get_status().value}")
            print("💡 This demonstrates handling driver connectivity issues")

        # Demo 9: Multiple Riders Request Same Driver
        print("\n📋 Demo 9: Multiple Riders Request Same Driver")
        print("-" * 50)

        # Set driver back to available
        driver1.set_status(DriverStatus.AVAILABLE)

        # Two riders request rides that could match the same driver
        ride9a = system.request_ride(alice.get_id(), Location(0.8, 0.8), Location(2.0, 2.0), RideType.AUTO, base_pricing)  # Close to driver1

        ride9b = system.request_ride(bob.get_id(), Location(1.2, 1.2), Location(2.5, 2.5), RideType.AUTO, base_pricing)  # Also close to driver1

        if ride9a and ride9b:
            print(f"💰 Ride A fare: ₹{ride9a.get_fare():.2f}")
            print(f"💰 Ride B fare: ₹{ride9b.get_fare():.2f}")

            # Driver accepts the first ride
            system.accept_ride(driver1.get_id(), ride9a)
            print(f"📊 Ride A state: {ride9a.get_status().value}")

            # Try to accept the second ride (should fail)
            print("🚫 Trying to accept second ride with same driver...")
            system.accept_ride(driver1.get_id(), ride9b)
            print(f"📊 Ride B state: {ride9b.get_status().value}")
            print("💡 This demonstrates driver capacity management")

        # Summary
        print("\n🎯 Design Patterns Demonstrated:")
        print("=" * 40)
        print("✅ Singleton Pattern - RideSharingSystem instance")
        print("✅ Factory Pattern - Vehicle creation")
        print("✅ Strategy Pattern - Driver matching & pricing")
        print("✅ Decorator Pattern - Pricing calculations")
        print("✅ Observer Pattern - Ride notifications")
        print("✅ State Pattern - Ride state transitions")
        print("✅ Builder Pattern - Location objects")
        print("✅ Error Handling - No available drivers")
        print("✅ Edge Cases - Ride cancellations & driver issues")

        # Display Driver Earnings and Ride History
        print("\n💰 Driver Earnings & Ride History:")
        print("=" * 50)

        drivers = [driver1, driver2, driver3, driver4]
        for driver in drivers:
            print(f"\n🚗 {driver.get_name()} ({driver.get_vehicle().get_model()})")
            print(f"   💵 Total Earnings: ₹{driver.get_total_earnings():.2f}")
            print(f"   📋 Rides Completed: {len(driver.get_ride_history())}")
            if driver.get_ride_history():
                print("   🎯 Recent Rides:")
                for ride in driver.get_ride_history():
                    print(f"      • Ride {ride.get_id()[:8]}... - ₹{ride.get_fare():.2f} ({ride.get_status().value})")

        print(f"\n👥 Rider Ride History:")
        print("=" * 30)
        riders = [alice, bob]
        for rider in riders:
            print(f"\n🚶 {rider.get_name()}")
            print(f"   📋 Rides Taken: {len(rider.get_ride_history())}")
            if rider.get_ride_history():
                print("   🎯 Ride History:")
                for ride in rider.get_ride_history():
                    driver_name = ride.get_driver().get_name() if ride.get_driver() else "No Driver"
                    print(f"      • Ride {ride.get_id()[:8]}... - ₹{ride.get_fare():.2f} with {driver_name} ({ride.get_status().value})")

        print(f"\n📊 Final Statistics:")
        print(f"   • Total rides completed: 5")
        print(f"   • Drivers available: {len([d for d in drivers if d.get_status() == DriverStatus.AVAILABLE])}")
        print(f"   • Riders registered: 2")
        print(f"   • Total platform revenue: ₹{sum([d.get_total_earnings() * 0.25 for d in drivers]):.2f} (25% commission)")


if __name__ == "__main__":
    RideSharingSystemDemo.run()
