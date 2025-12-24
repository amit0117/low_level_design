# Traffic Signal Control System

A scalable traffic signal control system for multi-road intersections using object-oriented design principles and design patterns.

## Design Patterns Used

### 1. **State Pattern** - Traffic Light States

- `TrafficLightState` (abstract base class)
- `RedState`, `YellowState`, `GreenState` (concrete states)
- Each state defines its behavior, duration, and valid transitions
- Ensures safe state transitions (Red → Yellow → Green → Red)

### 2. **Strategy Pattern** - Timing Strategies

- `TimingStrategy` (abstract base class)
- `FixedTimingStrategy` (implemented) - Fixed durations for each phase
- Allows runtime selection of timing algorithms
- Easy to extend with new strategies

## 📊 Entity Relationship Diagram

### Core Entities and Relationships

```
┌─────────────────────────────────────┐
│    TrafficController                │
│─────────────────────────────────────│
│ - intersection (Intersection)       │
│ - strategy (TimingStrategy)         │
│ - phases (List<SignalPhase>)        │
│ - current_phase_index               │
└──────┬──────────────────────────────┘
       │
       │ 1 (manages)
       │
       ▼
┌──────────────────────────────────────┐
│        Intersection                  │
│──────────────────────────────────────│
│ intersection_id                      │
│ roads (Dict<Direction, Road>)        │
│ traffic_lights (Dict<Direction,      │
│                 TrafficLight>)       │
│ current_phase (SignalPhase)          │
│ phase_history (List<SignalPhase>)    │
└──────┬───────────────────────────────┘
       │
       │ 1..* (has)
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│    Road     │ │ TrafficLight│ │ SignalPhase │
└─────────────┘ └─────────────┘ └─────────────┘

┌──────────────────────────────────────┐
│            Road                      │
│──────────────────────────────────────│
│ road_id                              │
│ direction (Direction)                │
│ num_lanes                            │
│ traffic_light (TrafficLight)         │
└──────────────────────────────────────┘

┌─────────────────────────────────────┐
│        TrafficLight                 │
│─────────────────────────────────────│
│ road (Road)                         │
│ state (TrafficLightState)           │
│ remaining_duration                  │
└──────┬──────────────────────────────┘
       │
       │ 1 (has)
       │
       ▼
┌─────────────────────────────────────┐
│    TrafficLightState                │
│─────────────────────────────────────│
│ (Abstract)                          │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┬──────────────┬
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  RedState   │ │ YellowState │ │ GreenState  │
└─────────────┘ └─────────────┘ └─────────────┘

┌──────────────────────────────────────┐
│        SignalPhase                   │
│──────────────────────────────────────│
│ phase_type (PhaseType)               │
│ allowed_directions (Set<Direction>)  │
│ duration                             │
└──────────────────────────────────────┘

┌─────────────────────────────────────┐
│      TimingStrategy                 │
│─────────────────────────────────────│
│ (Abstract)                          │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ▼
┌─────────────┐
│   Fixed     │
│   Timing    │
│  Strategy   │
└─────────────┘
```

### Entity Relationships

1. **TrafficController ↔ Intersection** (One-to-One)

   - Controller manages one Intersection
   - Intersection coordinates all traffic lights

2. **Intersection ↔ Road** (One-to-Many)

   - An Intersection has multiple Roads
   - Each Road belongs to one Intersection

3. **Intersection ↔ TrafficLight** (One-to-Many)

   - An Intersection has multiple TrafficLights
   - Each TrafficLight belongs to one Intersection

4. **Road ↔ TrafficLight** (One-to-One)

   - Each Road has one TrafficLight
   - TrafficLight controls traffic on that Road

5. **TrafficLight ↔ TrafficLightState** (One-to-One)

   - Each TrafficLight has one current State
   - State transitions: Red → Yellow → Green → Red

6. **TrafficController ↔ SignalPhase** (One-to-Many)

   - Controller manages multiple SignalPhases
   - Phases define which roads can be green simultaneously

7. **TrafficController ↔ TimingStrategy** (One-to-One)

   - Controller uses one TimingStrategy
   - Strategy determines phase durations

8. **SignalPhase ↔ Road** (Many-to-Many, via allowed_directions)
   - A SignalPhase allows certain Directions (Roads)
   - Multiple Roads can be in same phase

## 🔄 Data Flow Diagrams

### 1. Traffic Signal Control Flow

```
┌──────────┐
│  System  │
└────┬─────┘
     │
     │ 1. tick(current_time)
     ▼
┌─────────────────┐
│TrafficController│
└────┬────────────┘
     │
     │ 2. intersection.tick()
     │ 3. Check phase duration
     │ 4. Calculate next phase
     ▼
┌─────────────────┐
│ TimingStrategy  │
└────┬────────────┘
     │
     │ 5. calculate_duration()
     │ 6. Get next phase
     ▼
┌─────────────────┐
│  SignalPhase    │
└────┬────────────┘
     │
     │ 7. intersection.transition_phase()
     │ 8. Update traffic lights
     ▼
┌─────────────────┐
│ TrafficLights   │
│  (State Updated)│
└─────────────────┘
```

### 2. Phase Transition Flow

```
┌──────────┐
│Controller│
└────┬─────┘
     │
     │ 1. transition_phase(new_phase)
     ▼
┌─────────────────┐
│  Intersection   │
└────┬────────────┘
     │
     │ 2. can_transition()
     │ 3. Check conflicts
     │ 4. If safe, transition
     ▼
┌─────────────────┐
│  SignalPhase    │
└────┬────────────┘
     │
     │ 5. Update allowed directions
     │ 6. Update traffic lights
     ▼
┌─────────────────┐
│ TrafficLights   │
│  - RedState     │
│  - YellowState  │
│  - GreenState   │
└─────────────────┘
```

### 3. Traffic Light State Transition Flow

```
┌──────────┐
│Controller│
└────┬─────┘
     │
     │ 1. transition_to(new_state)
     ▼
┌─────────────────┐
│ TrafficLight    │
└────┬────────────┘
     │
     │ 2. state.transition_to()
     │ 3. Validate transition
     │ 4. Update state
     │ 5. Set duration
     ▼
┌────────────────────┐
│ TrafficLightState  │
│  (Red/Yellow/Green)│
└────┬───────────────┘
     │
     │ 6. State-specific behavior
     │ 7. Timer countdown
     │ 8. Auto-transition when expired
     ▼
┌─────────────────┐
│  Next State     │
└─────────────────┘
```

### 4. Complete System Interaction Flow

```
┌──────────────┐
│   Client     │
│  (demo.py)   │
└──────┬───────┘
       │
       │ All Operations
       ▼
┌─────────────────────────────────────┐
│    TrafficController                │
│  - Phase Management                 │
│  - Timing Strategy                  │
│  - Intersection Coordination        │
└──────┬──────────────────────────────┘
       │
       │
       ▼
┌─────────────────────────────────────┐
│        Intersection                 │
│  - Road Management                  │
│  - Traffic Light Coordination       │
│  - Conflict Prevention              │
└──────┬──────────────────────────────┘
       │
       ├──────────────────┬──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│    Roads    │  │ TrafficLights│  │ SignalPhases │
│  - Direction│  │  - State     │  │  - Allowed   │
│  - Lanes    │  │  - Duration  │  │    Directions│
└─────────────┘  └──────────────┘  └──────────────┘
       │                  │
       │                  │
       ▼                  ▼
┌─────────────┐  ┌────────────────┐
│ TrafficLight│  │ TimingStrategy │
│  State      │  │  - Fixed       │
│  - Red      │  │  - Actuated    │
│  - Yellow   │  │  - Adaptive    │
│  - Green    │  │                │
└─────────────┘  └────────────────┘
```

## 📋 Entity Attributes Summary

### TrafficController Entity

- `intersection`: Reference to Intersection
- `strategy`: TimingStrategy object
- `phases`: List of SignalPhase objects
- `current_phase_index`: Current phase index
- `phase_start_time`: When current phase started

### Intersection Entity

- `intersection_id`: Unique identifier
- `roads`: Dictionary mapping Direction to Road
- `traffic_lights`: Dictionary mapping Direction to TrafficLight
- `current_phase`: Current active SignalPhase
- `phase_history`: List of previous phases

### Road Entity

- `road_id`: Unique identifier
- `direction`: Direction (NORTH, SOUTH, EAST, WEST)
- `num_lanes`: Number of lanes
- `traffic_light`: Reference to TrafficLight

### TrafficLight Entity

- `road`: Reference to Road
- `state`: TrafficLightState object
- `remaining_duration`: Time remaining in current state

### TrafficLightState Entity (Abstract)

- `RedState`: Red light state
- `YellowState`: Yellow light state
- `GreenState`: Green light state

### SignalPhase Entity

- `phase_type`: PhaseType (NORTH_SOUTH_GREEN, EAST_WEST_GREEN, ALL_RED, EMERGENCY_PHASE)
- `allowed_directions`: Set of allowed Directions
- `duration`: Phase duration in seconds

### TimingStrategy Entity (Abstract)

- `FixedTimingStrategy`: Fixed durations for each phase

## Core Entities

### TrafficLight

- Holds current state and delegates behavior to state objects
- Manages state transitions safely
- Methods: `transition_to()`, `get_current_state()`, `get_remaining_duration()`

### TrafficLightState

- Abstract base class for traffic light states
- Each state defines transition rules and behavior
- Prevents unsafe transitions

### SignalPhase

- Defines which roads can have green simultaneously
- Contains conflict matrix to prevent conflicting greens
- Manages phase duration and transition rules

### Road

- Represents a road at the intersection
- Has direction (North, South, East, West)
- Contains lanes and associated TrafficLight

### Intersection

- Manages multiple Roads and TrafficLights
- Enforces safety rules (no conflicting greens)
- Coordinates phase transitions

### TrafficController

- Central coordinator
- Selects appropriate TimingStrategy
- Manages Intersection and phase transitions

### TimingStrategy

- Abstract base class for timing algorithms
- `FixedTimingStrategy`: Fixed durations for each phase

## Features Implemented

- ✅ Control traffic flow at intersection with multiple roads and lanes
- ✅ Support standard signals: Red, Yellow, Green
- ✅ Configurable signal durations
- ✅ Safe and smooth transitions between signals (no conflicting green signals)
- ✅ Extensible design for future features

## Missing Features (Can be Added Later)

### Sensors (Observer Pattern)

- `Sensor` (abstract base class)
- `VehicleSensor` - Detects vehicles waiting at intersection
- `PedestrianSensor` - Detects pedestrian button presses
- `EmergencySensor` - Detects emergency vehicles
- Sensors notify TrafficController using Observer pattern

### Additional Timing Strategies

- `ActuatedTimingStrategy` - Adjusts durations based on vehicle detection
- `EmergencyPriorityStrategy` - Immediate preemption for emergency vehicles
- AI-based timing strategies
- Adaptive timing based on traffic patterns

### Additional Features

- Pedestrian phases
- Multi-intersection coordination
- Real-time traffic monitoring
- Historical data analysis
- Dynamic timing adjustment based on traffic density

## Usage

```python
from app.models.intersection import Intersection
from app.models.road import Road
from app.models.traffic_controller import TrafficController
from app.models.enums import Direction

# Create intersection
intersection = Intersection("INTERSECTION_1")

# Create roads
north_road = Road("NORTH_ROAD", Direction.NORTH, num_lanes=2)
south_road = Road("SOUTH_ROAD", Direction.SOUTH, num_lanes=2)
east_road = Road("EAST_ROAD", Direction.EAST, num_lanes=2)
west_road = Road("WEST_ROAD", Direction.WEST, num_lanes=2)

# Add roads to intersection
intersection.add_road(north_road)
intersection.add_road(south_road)
intersection.add_road(east_road)
intersection.add_road(west_road)

# Create controller
controller = TrafficController(intersection)

# Run simulation
for t in range(100):
    controller.tick(t)
```

## Running the Demo

```bash
python3 demo.py
```

## Architecture

```
trafficSignalSystem/
├── app/
│   ├── models/
│   │   ├── traffic_light.py      # TrafficLight entity
│   │   ├── road.py               # Road entity
│   │   ├── intersection.py       # Intersection management
│   │   ├── signal_phase.py       # SignalPhase definitions
│   │   ├── traffic_controller.py # Central TrafficController
│   │   └── enums.py              # Enumerations
│   ├── states/
│   │   └── traffic_light_state.py # State Pattern (RedState, YellowState, GreenState)
│   └── strategies/
│       └── timing_strategy.py    # Strategy Pattern (FixedTimingStrategy)
└── demo.py                       # Demonstration
```

## Design Principles

- **SOLID Principles**: Single Responsibility, Open/Closed, Dependency Inversion
- **Separation of Concerns**: Clear boundaries between entities
- **Extensibility**: Easy to add new states, strategies, and features
- **Safety**: Conflict prevention ensures no conflicting green signals
- **Maintainability**: Clean code structure with clear responsibilities
