"""
Mermaid Diagrams for Elevator System - Low Level Design
"""

DATA_FLOW_DIAGRAM = """
```mermaid
graph TD
    Passenger[Passenger] -->|creates| Request[Request]
    Request -->|external| ExternalRequest[External Request - Floor Button]
    Request -->|internal| InternalRequest[Internal Request - Cabin Button]

    Request -->|handled by| ElevatorService[ElevatorService]
    ElevatorService -->|uses| SchedulingStrategy{Scheduling Strategy}
    SchedulingStrategy -->|FCFS| FCFS[FCFS Strategy]
    SchedulingStrategy -->|SSTF| SSTF[SSTF Strategy]
    SchedulingStrategy -->|SCAN| SCAN[SCAN Strategy]

    ElevatorService -->|manages| Elevator[Elevator]
    Elevator -->|stored in| ElevatorRepository[ElevatorRepository]
    Elevator -->|has| ElevatorState{Elevator State}
    ElevatorState -->|idle| IdleState[IdleState]
    ElevatorState -->|moving up| MovingUpState[MovingUpState]
    ElevatorState -->|moving down| MovingDownState[MovingDownState]

    Elevator -->|has| DoorStatus[DoorStatus]
    Elevator -->|moves between| Floor[Floor]
    Floor -->|stored in| FloorRepository[FloorRepository]

    Elevator -->|observed by| DisplayPanel[DisplayPanel Observer]
    DisplayPanel -->|shows| CurrentFloor[Current Floor]
    DisplayPanel -->|shows| Direction[Direction]

    Passenger -->|enters/exits| Elevator
```
"""

USER_FLOW_DIAGRAM = """
```mermaid
sequenceDiagram
    actor Passenger
    participant Floor
    participant ElevatorService
    participant Scheduler as SchedulingStrategy
    participant Elevator
    participant DisplayPanel

    Note over Elevator: State = IdleState

    Passenger->>Floor: Press UP/DOWN button (External Request)
    Floor->>ElevatorService: External request (floor, direction)
    ElevatorService->>Scheduler: Find best elevator
    Scheduler-->>ElevatorService: Assigned elevator

    ElevatorService->>Elevator: Move to requested floor
    Note over Elevator: State = MovingUpState / MovingDownState
    Elevator->>DisplayPanel: Update floor & direction
    DisplayPanel-->>Passenger: Show current position

    Elevator->>Elevator: Arrive at floor
    Note over Elevator: Doors = OPEN
    Passenger->>Elevator: Enter cabin

    Passenger->>Elevator: Press destination floor (Internal Request)
    Elevator->>ElevatorService: Internal request (destination)
    Note over Elevator: Doors = CLOSED

    ElevatorService->>Elevator: Move to destination
    Note over Elevator: State = MovingUpState / MovingDownState
    Elevator->>DisplayPanel: Update floor & direction

    Elevator->>Elevator: Arrive at destination
    Note over Elevator: Doors = OPEN
    Passenger->>Elevator: Exit cabin
    Note over Elevator: Doors = CLOSED

    alt No pending requests
        Note over Elevator: State = IdleState
    else More requests
        ElevatorService->>Scheduler: Get next request
        Scheduler-->>ElevatorService: Next floor
        ElevatorService->>Elevator: Continue to next floor
    end
```
"""

if __name__ == "__main__":
    print("=" * 60)
    print("DATA FLOW DIAGRAM")
    print("=" * 60)
    print(DATA_FLOW_DIAGRAM)
    print("=" * 60)
    print("USER FLOW DIAGRAM")
    print("=" * 60)
    print(USER_FLOW_DIAGRAM)
