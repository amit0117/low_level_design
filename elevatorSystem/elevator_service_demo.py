from app.services.elevator_service import ElevatorService
from app.models.enums import Direction
from app.strategies.elevator_scheduling_strategy import FCFS, SCAN, SSTF
import time


class ElevatorServiceDemo:
    @staticmethod
    def main():
        print("=== Elevator Service Demo ===\n")

        # Setup: A building with 4 elevators
        num_elevators = 4
        elevator_service = ElevatorService.get_instance(num_elevators)

        # Start the elevator system
        elevator_service.start()
        print("Elevator system started with 4 elevators.\n")

        # --- SIMULATION START ---

        # 1. External Request: User at floor 5 wants to go UP
        print("1. External Request: User at floor 5 wants to go UP")
        elevator_service.request_elevator(5, Direction.UP)
        time.sleep(0.5)

        # 2. Internal Request: User in elevator selects floor 10
        print("2. Internal Request: User in elevator selects floor 10")
        # Get the first elevator's ID for internal request
        elevators = elevator_service.elevator_repository.get_all_elevators()
        if elevators:
            elevator_service.select_floor(elevators[0].get_id(), 10)
        time.sleep(0.5)

        # 3. External Request: User at floor 3 wants to go DOWN
        print("3. External Request: User at floor 3 wants to go DOWN")
        elevator_service.request_elevator(3, Direction.DOWN)
        time.sleep(0.5)

        # 4. External Request: User at floor 8 wants to go UP
        print("4. External Request: User at floor 8 wants to go UP")
        elevator_service.request_elevator(8, Direction.UP)
        time.sleep(0.5)

        # 5. Internal Request: User in elevator selects floor 2
        print("5. Internal Request: User in elevator selects floor 2")
        # Get the second elevator's ID for internal request
        if len(elevators) > 1:
            elevator_service.select_floor(elevators[1].get_id(), 2)
        time.sleep(0.5)

        # 6. External Request: User at floor 1 wants to go UP
        print("6. External Request: User at floor 1 wants to go UP")
        elevator_service.request_elevator(1, Direction.UP)
        time.sleep(0.5)

        # 7. External Request: User at floor 9 wants to go DOWN (to test DOWN movement)
        print("7. External Request: User at floor 9 wants to go DOWN")
        elevator_service.request_elevator(9, Direction.DOWN)
        time.sleep(0.5)

        # Let the simulation run for a while to observe elevator movements
        print("\n--- Letting simulation run for 3 seconds ---")
        time.sleep(3)

        # Demonstrate different scheduling strategies
        print("\n--- Testing Different Scheduling Strategies ---")

        # Test FCFS Strategy
        print("\n8. Switching to FCFS (First Come First Serve) strategy")
        elevator_service.set_scheduling_strategy(FCFS())
        elevator_service.request_elevator(6, Direction.UP)
        time.sleep(1)

        # Test SSTF Strategy
        print("9. Switching to SSTF (Shortest Seek Time First) strategy")
        elevator_service.set_scheduling_strategy(SSTF())
        elevator_service.request_elevator(4, Direction.DOWN)
        time.sleep(1)

        # Test SCAN Strategy
        print("10. Switching back to SCAN (Elevator Algorithm) strategy")
        elevator_service.set_scheduling_strategy(SCAN())
        elevator_service.request_elevator(7, Direction.DOWN)
        time.sleep(1)

        # Let the simulation run for a bit more
        print("\n--- Letting simulation run for 2 more seconds ---")
        time.sleep(2)

        # Shutdown the system
        print("\n--- Shutting down elevator system ---")
        elevator_service.shutdown()

        # Wait a moment for elevators to stop
        print("Waiting for elevators to stop...")
        time.sleep(1)

        print("=== Demo Complete ===")
        print("All elevators have been stopped successfully!")


if __name__ == "__main__":
    ElevatorServiceDemo.main()
