import threading
import time
from parking_lot import ParkingLot
from app.models.floor import Floor
from app.models.parking_spot import ParkingSpot
from app.models.vehicle import Car, Motorcycle, Truck
from app.models.gate import EntryGate, ExitGate
from app.models.enums import VehicleType


def setup_parking_lot():
    parking_lot = ParkingLot.get_instance()

    floor1 = Floor(1)
    floor2 = Floor(2)
    floor3 = Floor(3)

    for i in range(1, 6):
        floor1.add_parking_spot(ParkingSpot(i, VehicleType.CAR))
        floor1.add_parking_spot(ParkingSpot(i + 5, VehicleType.MOTORCYCLE))

    for i in range(1, 6):
        floor2.add_parking_spot(ParkingSpot(i, VehicleType.CAR))
        floor2.add_parking_spot(ParkingSpot(i + 5, VehicleType.TRUCK))

    for i in range(1, 4):
        floor3.add_parking_spot(ParkingSpot(i, VehicleType.MOTORCYCLE))
        floor3.add_parking_spot(ParkingSpot(i + 3, VehicleType.CAR))

    parking_lot.add_floor(floor1)
    parking_lot.add_floor(floor2)
    parking_lot.add_floor(floor3)

    entry_gate1 = EntryGate(1)
    entry_gate2 = EntryGate(2)
    exit_gate1 = ExitGate(1)
    exit_gate2 = ExitGate(2)

    parking_lot.add_entry_gate(entry_gate1)
    parking_lot.add_entry_gate(entry_gate2)
    parking_lot.add_exit_gate(exit_gate1)
    parking_lot.add_exit_gate(exit_gate2)

    return parking_lot


def park_vehicle_thread(parking_lot, vehicle, gate_number, results, index):
    try:
        ticket = parking_lot.park_vehicle(vehicle, gate_number)
        if ticket:
            results[index] = {"success": True, "ticket_id": ticket.get_ticket_id(), "vehicle": vehicle.license_plate}
            print(
                f"✓ Vehicle {vehicle.license_plate} parked successfully. Ticket: {ticket.get_ticket_id()}, Floor: {ticket.get_floor_number()}, Spot: {ticket.get_parking_spot().get_spot_number()}"
            )
        else:
            results[index] = {"success": False, "reason": "No parking spot available"}
            print(f"✗ Vehicle {vehicle.license_plate} could not be parked - no spots available")
    except Exception as e:
        results[index] = {"success": False, "reason": str(e)}
        print(f"✗ Error parking vehicle {vehicle.license_plate}: {e}")


def test_concurrent_parking():
    print("\n" + "=" * 80)
    print("TEST 1: Concurrent Parking Access")
    print("=" * 80)

    parking_lot = setup_parking_lot()

    vehicles = [
        Car("MH12AB1234"),
        Car("MH12AB1235"),
        Car("MH12AB1236"),
        Car("MH12AB1237"),
        Car("MH12AB1238"),
        Car("MH12AB1239"),
        Motorcycle("MH12MC1234"),
        Motorcycle("MH12MC1235"),
        Truck("MH12TR1234"),
        Truck("MH12TR1235"),
    ]

    results = [None] * len(vehicles)
    threads = []

    for i, vehicle in enumerate(vehicles):
        gate_number = 1 if i % 2 == 0 else 2
        thread = threading.Thread(target=park_vehicle_thread, args=(parking_lot, vehicle, gate_number, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    successful = sum(1 for r in results if r and r.get("success"))
    print(f"\nResults: {successful}/{len(vehicles)} vehicles parked successfully")

    print("\nParking Lot Availability After Concurrent Parking:")
    parking_lot.display_availability()

    return results, parking_lot


def test_unparking(parking_lot, tickets):
    print("\n" + "=" * 80)
    print("TEST 2: Vehicle Exit and Payment")
    print("=" * 80)

    if not tickets:
        print("No tickets available for unparking test")
        return

    for i, ticket_info in enumerate(tickets):
        if ticket_info and ticket_info.get("success"):
            ticket_id = ticket_info["ticket_id"]
            exit_gate = 1 if i % 2 == 0 else 2

            print(f"\nExiting vehicle with ticket {ticket_id} through gate {exit_gate}")
            payment_response = parking_lot.unpark_vehicle(ticket_id, exit_gate)

            if payment_response:
                print(f"✓ Payment processed: Amount ₹{payment_response.get_amount()}, Status: {payment_response.get_status()}")
            else:
                print(f"✗ Payment failed")

    print("\nParking Lot Availability After Unparking:")
    parking_lot.display_availability()


def test_no_spots_available():
    print("\n" + "=" * 80)
    print("TEST 3: No Spots Available Scenario")
    print("=" * 80)

    parking_lot = ParkingLot.get_instance()

    floor = Floor(10)
    parking_lot.add_floor(floor)

    spot = ParkingSpot(1, VehicleType.CAR)
    floor.add_parking_spot(spot)

    car1 = Car("MH12AB9999")
    ticket1 = parking_lot.park_vehicle(car1, 1)

    if ticket1:
        print(f"✓ Vehicle {car1.license_plate} parked. Ticket: {ticket1.get_ticket_id()}")
    else:
        print(f"✗ Vehicle {car1.license_plate} could not be parked - no spots available")

    car2 = Car("MH12AB9998")
    ticket2 = parking_lot.park_vehicle(car2, 1)

    if ticket2:
        print(f"✓ Vehicle {car2.license_plate} parked. Ticket: {ticket2.get_ticket_id()}")
    else:
        print(f"✗ Vehicle {car2.license_plate} could not be parked - no spots available")

    print("\nFilling all available CAR spots...")
    all_cars = [Car(f"MH{i:02d}AB1111") for i in range(1, 30)]
    parked_count = 0
    failed_count = 0

    for car in all_cars:
        ticket = parking_lot.park_vehicle(car, 1)
        if ticket:
            parked_count += 1
        else:
            failed_count += 1

    print(f"Parked: {parked_count}, Failed: {failed_count}")

    car_final = Car("MH99AB9999")
    ticket_final = parking_lot.park_vehicle(car_final, 1)

    if ticket_final:
        print(f"✓ Vehicle {car_final.license_plate} parked. Ticket: {ticket_final.get_ticket_id()}")
    else:
        print(f"✗ Vehicle {car_final.license_plate} could not be parked - no spots available")


def test_mixed_vehicle_types():
    print("\n" + "=" * 80)
    print("TEST 4: Mixed Vehicle Types")
    print("=" * 80)

    parking_lot = ParkingLot.get_instance()

    vehicles = [
        Car("DL01AB1111"),
        Motorcycle("DL01MC2222"),
        Truck("DL01TR3333"),
        Car("DL01AB4444"),
        Motorcycle("DL01MC5555"),
    ]

    tickets = []
    for vehicle in vehicles:
        ticket = parking_lot.park_vehicle(vehicle, 1)
        if ticket:
            tickets.append(ticket)
            print(
                f"✓ {vehicle.__class__.__name__} {vehicle.license_plate} parked on Floor {ticket.get_floor_number()}, Spot {ticket.get_parking_spot().get_spot_number()}"
            )
        else:
            print(f"✗ {vehicle.__class__.__name__} {vehicle.license_plate} could not be parked")

    print("\nCurrent Availability:")
    parking_lot.display_availability()


def test_concurrent_booking_same_spots():
    print("\n" + "=" * 80)
    print("TEST 5: Concurrent Booking - Attempting to Book Same Spots")
    print("=" * 80)

    parking_lot = ParkingLot.get_instance()

    cars = [Car(f"KA{i:02d}AB1234") for i in range(1, 8)]

    results = [None] * len(cars)
    threads = []

    def park_car(index):
        try:
            vehicle = cars[index]
            ticket = parking_lot.park_vehicle(vehicle, 1)
            if ticket:
                results[index] = {"success": True, "ticket_id": ticket.get_ticket_id()}
                print(f"✓ Car {vehicle.license_plate} parked - Floor {ticket.get_floor_number()}, Spot {ticket.get_parking_spot().get_spot_number()}")
            else:
                results[index] = {"success": False}
                print(f"✗ Car {vehicle.license_plate} - No spot available")
        except Exception as e:
            results[index] = {"success": False, "error": str(e)}
            print(f"✗ Car {cars[index].license_plate} - Error: {e}")

    for i in range(len(cars)):
        thread = threading.Thread(target=park_car, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    successful = sum(1 for r in results if r and r.get("success"))
    print(f"\nResults: {successful}/{len(cars)} cars parked successfully (expecting some failures due to limited spots)")

    print("\nFinal Parking Lot State:")
    parking_lot.display_availability()


def main():
    print("=" * 80)
    print("PARKING LOT SYSTEM DEMO")
    print("=" * 80)

    parking_lot = setup_parking_lot()

    print("\nInitial Parking Lot Setup:")
    print(f"Floors: {len(parking_lot.get_floors())}")
    for floor in parking_lot.get_floors():
        print(f"  Floor {floor.get_floor_number()}: {len(floor.get_parking_spots())} spots")

    print("\nInitial Availability:")
    parking_lot.display_availability()

    results, parking_lot = test_concurrent_parking()

    tickets = [r for r in results if r and r.get("success")]
    if tickets:
        time.sleep(1)
        test_unparking(parking_lot, tickets)

    test_no_spots_available()

    test_mixed_vehicle_types()

    test_concurrent_booking_same_spots()

    print("\n" + "=" * 80)
    print("DEMO COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()
