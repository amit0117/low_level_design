"""
Mermaid Diagrams for Traffic Signal System - Low Level Design
"""

DATA_FLOW_DIAGRAM = """
```mermaid
graph TD
    TrafficController[TrafficController] -->|manages| Intersection[Intersection]
    Intersection -->|has 4| Road{Roads}
    Road -->|north| NorthRoad[North Road]
    Road -->|south| SouthRoad[South Road]
    Road -->|east| EastRoad[East Road]
    Road -->|west| WestRoad[West Road]

    NorthRoad -->|has| NorthLight[TrafficLight N]
    SouthRoad -->|has| SouthLight[TrafficLight S]
    EastRoad -->|has| EastLight[TrafficLight E]
    WestRoad -->|has| WestLight[TrafficLight W]

    NorthLight -->|has| LightState{Traffic Light State}
    LightState -->|red| RedState[RedState]
    LightState -->|yellow| YellowState[YellowState]
    LightState -->|green| GreenState[GreenState]

    TrafficController -->|uses| TimingStrategy[TimingStrategy]
    TimingStrategy -->|fixed| FixedTiming[FixedTimingStrategy]

    TrafficController -->|coordinates| PhaseManager[PhaseManager]
    PhaseManager -->|manages| SignalPhase[SignalPhase]
    SignalPhase -->|has| PhaseType[PhaseType]
    SignalPhase -->|determines| ActiveRoads[Active Green Roads]
    SignalPhase -->|sets duration| Duration[Phase Duration]
```
"""

USER_FLOW_DIAGRAM = """
```mermaid
sequenceDiagram
    participant Controller as TrafficController
    participant PhaseManager
    participant Phase as SignalPhase
    participant NorthLight as TrafficLight N
    participant SouthLight as TrafficLight S
    participant EastLight as TrafficLight E
    participant WestLight as TrafficLight W

    Controller->>PhaseManager: Initialize phases
    PhaseManager->>Phase: Create Phase 1 (N-S Green)
    PhaseManager->>Phase: Create Phase 2 (E-W Green)

    loop Traffic Signal Cycle
        Controller->>PhaseManager: Activate Phase 1
        PhaseManager->>Phase: Get Phase 1 config

        Phase->>NorthLight: Set GREEN
        Note over NorthLight: State = GreenState
        Phase->>SouthLight: Set GREEN
        Note over SouthLight: State = GreenState
        Phase->>EastLight: Set RED
        Note over EastLight: State = RedState
        Phase->>WestLight: Set RED
        Note over WestLight: State = RedState

        Note over Controller: Wait for phase duration (Fixed Timing)

        Phase->>NorthLight: Set YELLOW
        Note over NorthLight: State = YellowState
        Phase->>SouthLight: Set YELLOW
        Note over SouthLight: State = YellowState

        Note over Controller: Yellow transition period

        Phase->>NorthLight: Set RED
        Note over NorthLight: State = RedState
        Phase->>SouthLight: Set RED
        Note over SouthLight: State = RedState

        Controller->>PhaseManager: Activate Phase 2
        PhaseManager->>Phase: Get Phase 2 config

        Phase->>EastLight: Set GREEN
        Note over EastLight: State = GreenState
        Phase->>WestLight: Set GREEN
        Note over WestLight: State = GreenState

        Note over Controller: Wait for phase duration

        Phase->>EastLight: Set YELLOW
        Phase->>WestLight: Set YELLOW
        Note over Controller: Yellow transition
        Phase->>EastLight: Set RED
        Phase->>WestLight: Set RED
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
