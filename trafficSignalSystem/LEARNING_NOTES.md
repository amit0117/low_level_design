# Traffic Signal Control System - Learning Notes

## 1. Traffic Light Controller - Overview

### Definition

A device that governs signal operation at intersections. It determines how long each light stays green, yellow, or red based on preset or real-time logic.

### Evolution

The basic purpose hasn't changed much, but the technology has significantly advanced, making way for greater precision and adaptability.

---

## 2. Types of Traffic Light Controllers

### 2.1 Fixed-Time Controllers

**Characteristics:**

- Basic form of traffic management
- Does not respond to traffic volume
- Follows a programmed sequence
- **Reliable and simple**

**Use Cases:**

- Low-traffic intersections
- Predictable intersections

**Example:**

- Green (30s) → Yellow (4s) → Red (34s)

### 2.2 Actuated Controllers

**Characteristics:**

- **Smart Timing**
- Adjusts signal timing based on actual traffic conditions
- Uses input from sensors or cameras
- Detects approaching vehicles and modifies signal timing accordingly

**Pros:**

- Responsive to real-time demand
- Reduces idle time and unnecessary delays
- Enhances flow during peak hours

**Used At:**

- Suburban intersections
- Areas near shopping centres and schools

**How They Work:**

- Use inductive loops (built underneath the intersection)
- Use cameras, IR/Radar sensors for traffic tracking
- Pedestrian push buttons
- Extended green if vehicles are detected
- Skip phase if no demand

**Factors Affecting Light Changes:**

- Traffic density per lane
- Time of day (peak vs off-peak)

### 2.3 Adaptive Controllers

**Characteristics:**

- **Real-time Intelligence**
- Most advanced type
- Don't just react to vehicles - they analyze patterns, predict congestion, and modify traffic signal timing in real-time using complex algorithms

**How Adaptive Controllers Work:**

- Integrate a network of detectors, cameras, and processors
- Collect data across multiple intersections
- Data is analyzed centrally or locally
- Adapt signal phasing and timing based on current and predicted traffic flow

**Pros:**

- Maximizes traffic efficiency across entire corridors
- Responds to incidents, congestion, and time-of-day patterns
- Provides best balance of throughput and safety

**Should Be Used At:**

- Metropolitan intersections
- High-density corridors (linear areas defined by one or more modes of transportation crossing the limit of more than one city/country like highways, railroads, or public transit which share a common destination)
- Smart city infrastructure

---

## 3. Signal Phase in Traffic System

### Definition

A logical unit of time during which a specific, non-conflicting set of traffic movement is allowed to proceed while all conflicting movements are stopped.

**Key Point:** Signal phase defines who is allowed to move and for how long.

### Signal Phase vs Light Color

- **Signal Phase ≠ Light Color**
- **Signal Phase:** It is a policy
- **Light Color:** It is a mechanism
- **Phases decide colors, not the other way around**

**Example:**

- Phase: NS-Straight
  - NS lights → Green
  - EW lights → Red

### 4-Way Intersection Movements

- NS-Straight, NS-Left
- EW-Straight, EW-Left
- Pedestrian movements

### Signal Phase Properties

- Allowed movements []
- Min green time
- Max green time
- Yellow time
- All red clearance time
- Next phases []

**Important:** Signal phase doesn't care about sensors or lights directly.

### How Phase is Used in System

```
Controller selects a phase
    ↓
Phase maps movements
    ↓
Light enters Green
    ↓
Light colors
    ↓
After min time, controller may extend/terminate
    ↓
Yellow
    ↓
All Red
    ↓
Next Phase
```

### Example Signal Phase

**Phase 1: NS-Straight**

- Allowed: N→S, S→N
- Duration: 30-60s
- EW = RED

---

## 4. Entities for Traffic System

### Core Entities

1. **Traffic Light**
2. **Signal Phase**
3. **Intersection**
4. **Lane**
5. **Sensor**
6. **Timer**
7. **Controller**

### Responsibilities of Each Entity

#### (a) Traffic Light

- Current color display
- Transition logic
- Maintain current state
- Execute state transition
- No knowledge of other lights

#### (b) Signal Phase

- Allowed movements (NS, E-W, pedestrian)
- Duration constraints
- Defines who can move and for how long

#### (c) Intersection

- Owns multiple traffic lights
- Prevents conflicting greens
- Coordinates all traffic lights
- Resolves conflicts
- Enforces safety rules

#### (d) Sensor

- Report vehicle/pedestrian presence
- Detect events
- Notify mediator (controller)

#### (e) Controller

- Decide next phase
- Apply timing rules
- Centralize decision making

---

## 5. Conflicting Directions

### Key Rule

**Red light time for 1 direction = Green + Yellow of conflicting direction**

### Granularity of Movement Model

The number of conflicting movements depends on how granular the movement model is:

#### Coarse-Grained (Fixed Time)

- NS-Straight
- EW-Straight

#### Medium-Grained (Most Real Intersections)

- NS-Straight, NS-Left
- EW-Straight, EW-Left
- Pedestrian+NS, Pedestrian-EW

#### Recommended for Interview

- NS-Straight
- EW-Straight
- Pedestrian

---

## 6. Mediator Pattern

### When Mediator Pattern is Needed

**NEEDED:**

- At an intersection, multiple components are coordinating:
  - NS-Signal, EW-Signal
  - Pedestrian-Signal
  - Emergency-Override
  - Multiple sensors
- Direct communication is unmanageable

**When Mediator is NOT Needed:**

- Single traffic light
- Fixed time cycle
- No sensor or cross-direction coordination
- In this case, a controller directly managing traffic light is sufficient

### Intersection Controller as Mediator

**Responsibilities:**

- Coordinate all traffic lights
- Resolve conflicts
- Enforce safety rules
- Centralize decision making

**Key Principle:** Components don't talk to each other directly.

### Colleagues (Components)

**Traffic Light:**

- Maintain current state
- Execute state transition
- No knowledge of other lights

**Sensor:**

- Detect events
- Notify mediator

**Interaction:**

```
[Sensor, Button, Light] → Intersection Controller (Mediator)
```

---

## 7. Design Patterns

### ① State Pattern

- Represents signal states
- **States:** RedState, GreenState, YellowState
- Each state knows its duration and next state

### ② Strategy Pattern

**Context:** For timing of traffic light

**Strategies:**

- Fixed Timing Strategy
- Actuated Timing Strategy
- Adaptive Timing Strategy

### ③ Observer Pattern

- Sensors, camera, inductive loops notify controllers
- One-to-many dependency between sensors and controller

---

## 8. Data Flow

### High-Level Data Flow

```
[SENSOR]
    ↓ (vehicle count, pedestrian request)
[CONTROLLER]
    ↓ (select timing strategy)
[TIMING STRATEGY]
    ↓ (duration, next phase)
[SIGNAL PHASE]
    ↓
[TRAFFIC LIGHT STATE]
```

---

## 9. Execution Flow

### Loop Every Second:

1. Read sensors
2. Controller decides next phase
3. Traffic light transitions if timer expires

---

## 10. Traffic Signal Basics

### Signal Sequence

**Red → Green → Amber (Yellow)**

### Key Rule

Red light time for 1 direction = Green + Yellow of conflicting direction

### Signal Change Mechanisms

#### Fixed Time Signals

- Uses predefined intervals
- No awareness of traffic volume
- Used at low-traffic or predictable intersections

#### Actuated Signals

- Changes based on sensor data
- Uses inductive loops, cameras, IR/Radar sensors
- Pedestrian push buttons
- Extended green if vehicles detected
- Skip phase if no demand

#### Adaptive Signals

- Uses real-time traffic data
- Centralized or AI-based control
- Used in smart cities

---

## 11. Emergency Vehicle Handling

### Emergency Vehicle Detection

- Emergency vehicles (VIP/Ambulance) release special radiation/rays
- Traffic sensors detect these signals
- Provides immediate green signal for emergency vehicle
- Overrides normal traffic flow

---

## 12. System Architecture Summary

### Recommended Design Patterns

1. **State Pattern** - For traffic light states
2. **Strategy Pattern** - For timing strategies
3. **Observer Pattern** - For sensor notifications
4. **Mediator Pattern** - For intersection coordination (when multiple components interact)

### Key Principles

- Signal phase is a policy, not a mechanism
- Phases decide colors, not the other way around
- Controller centralizes decision making
- Components communicate through mediator, not directly
- Safety: Prevent conflicting green signals
- Flexibility: Support fixed, actuated, and adaptive timing

### System Flow

1. Sensors detect traffic/pedestrian presence
2. Controller receives sensor data
3. Controller selects appropriate timing strategy
4. Strategy calculates duration and next phase
5. Signal phase defines allowed movements
6. Traffic lights transition based on phase
7. Process repeats every second

---

## 13. Implementation Considerations

### For Interview/Simple Implementation

- Use coarse-grained movement model (NS-Straight, EW-Straight, Pedestrian)
- Start with Fixed Timing Strategy
- Can extend to Actuated and Adaptive later
- Mediator pattern needed when multiple signals/sensors interact

### For Production System

- Medium-grained movement model
- Support all three timing strategies
- Implement sensor integration
- Emergency vehicle priority
- Multi-intersection coordination
- Real-time traffic analysis

---

## 14. Key Takeaways

1. **Traffic controllers** have evolved from simple fixed-time to intelligent adaptive systems
2. **Signal phases** are logical units that define traffic movement policies
3. **Design patterns** (State, Strategy, Observer, Mediator) are essential for clean architecture
4. **Safety** is paramount - no conflicting green signals
5. **Flexibility** allows system to adapt from simple fixed-time to complex adaptive control
6. **Scalability** supports single intersection to smart city networks
