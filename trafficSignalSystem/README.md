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
