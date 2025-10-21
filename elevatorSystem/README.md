# Elevator Control System

A comprehensive Low-Level Design (LLD) implementation of an elevator control system using Python, demonstrating advanced object-oriented design principles and design patterns.

## 🏗️ System Architecture

This elevator system implements a robust, scalable architecture using multiple design patterns:

### Core Design Patterns Used

1. **State Pattern** - Manages elevator states (Idle, MovingUp, MovingDown)
2. **Strategy Pattern** - Implements different elevator scheduling algorithms
3. **Observer Pattern** - Notifies display panels about elevator status changes
4. **Singleton Pattern** - Ensures single instance of elevator service
5. **Repository Pattern** - Manages elevator and floor data access

### Key Components

```
app/
├── models/           # Core domain entities
│   ├── elevator.py   # Elevator entity with state management
│   ├── request.py    # Request model for elevator calls
│   ├── enums.py      # System enumerations
│   └── display_panel.py # Display panel observer
├── states/           # State pattern implementation
│   └── elevator_state.py # Idle, MovingUp, MovingDown states
├── strategies/       # Strategy pattern for scheduling
│   └── elevator_scheduling_strategy.py # SCAN, FCFS, SSTF algorithms
├── services/         # Business logic layer
│   └── elevator_service.py # Main elevator service
├── repositories/     # Data access layer
│   ├── elevator_repository.py
│   └── floor_repository.py
└── observers/       # Observer pattern implementation
    ├── base_observer.py
    ├── base_subject.py
    └── elevator_observer.py
```

## 🚀 Features

### Elevator States

- **Idle State**: Elevator waiting for requests
- **Moving Up State**: Elevator ascending to serve up requests
- **Moving Down State**: Elevator descending to serve down requests

### Scheduling Algorithms

- **SCAN (Elevator Algorithm)**: Efficient bidirectional scanning
- **FCFS (First Come First Serve)**: Simple request ordering
- **SSTF (Shortest Seek Time First)**: Minimizes travel distance

### Request Types

- **External Requests**: Floor button calls (UP/DOWN)
- **Internal Requests**: Destination floor selection inside elevator

### Real-time Monitoring

- Live elevator position tracking
- State transition logging
- Display panel notifications

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- No external dependencies required (pure Python implementation)

### Running the System

1. **Basic Demo** (shows all elevator states):

```bash
cd low_level_design/elevatorSystem
python3 elevator_service_demo.py
```

2. **Better Demo** (designed to showcase all states clearly):

```bash
python3 better_demo.py
```

## 📊 System Behavior

### State Transitions

```
Idle State
    ↓ (UP requests)
MovingUp State
    ↓ (no more UP requests)
Idle State
    ↓ (DOWN requests)
MovingDown State
    ↓ (no more DOWN requests)
Idle State
```

### Request Processing Flow

1. **External Request**: User presses floor button
2. **Elevator Selection**: Scheduling strategy selects best elevator
3. **Request Addition**: Request added to elevator's queue
4. **State Transition**: Elevator transitions to appropriate state
5. **Movement**: Elevator moves floor by floor
6. **Request Completion**: Request removed when floor reached
7. **State Check**: Elevator checks for remaining requests

## 🎯 Design Principles Applied

### SOLID Principles

- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Easy to add new scheduling strategies
- **Liskov Substitution**: State implementations are interchangeable
- **Interface Segregation**: Clean, focused interfaces
- **Dependency Inversion**: Depends on abstractions, not concretions

### Additional Principles

- **DRY (Don't Repeat Yourself)**: Reusable components
- **KISS (Keep It Simple, Stupid)**: Clear, understandable code
- **YAGNI (You Aren't Gonna Need It)**: Only implemented required features

## 🔧 Configuration

### System Parameters

- **Number of Elevators**: Configurable (default: 4)
- **Building Floors**: 0-10 (configurable)
- **Elevator Capacity**: Configurable per elevator
- **Movement Speed**: 1 second per floor (configurable)

### Scheduling Strategy Selection

```python
# Switch scheduling strategies at runtime
elevator_service.set_scheduling_strategy(SCAN())    # Default
elevator_service.set_scheduling_strategy(FCFS())    # First Come First Serve
elevator_service.set_scheduling_strategy(SSTF())    # Shortest Seek Time First
```

## 📈 Performance Characteristics

### SCAN Algorithm

- **Best for**: High-traffic scenarios
- **Efficiency**: O(n) where n = number of floors
- **Fairness**: Good - serves requests in order

### FCFS Algorithm

- **Best for**: Simple scenarios
- **Efficiency**: O(1) per request
- **Fairness**: Excellent - strict chronological order

### SSTF Algorithm

- **Best for**: Minimizing travel time
- **Efficiency**: O(n) per request
- **Fairness**: Poor - may starve distant requests

## 🧪 Testing Scenarios

The system includes comprehensive demo scenarios:

1. **Mixed Request Types**: External + Internal requests
2. **State Transitions**: All three elevator states
3. **Scheduling Strategies**: All three algorithms
4. **Concurrent Operations**: Multiple elevators working simultaneously
5. **Edge Cases**: Boundary conditions and error handling

## 🔍 Debugging & Monitoring

### Debug Output

The system provides detailed debug information:

```
DEBUG: Elevator abc123... transitioning to MovingUpState (UP requests: 3)
DEBUG: Elevator abc123... transitioning from MovingUpState to IdleState
DEBUG SCAN: Selected elevator abc123...
```

### Display Panel Messages

```
[DISPLAY PANEL]: Elevator abc123... is now at floor 5 and is moving up
[DISPLAY PANEL]: Elevator abc123... is now at floor 5 and is idle
[DISPLAY PANEL]: Elevator abc123... is now at floor 4 and is moving down
```

## 🚀 Future Enhancements

### Potential Improvements

- **Load Balancing**: Distribute passengers evenly
- **Predictive Scheduling**: AI-based request prediction
- **Energy Optimization**: Minimize power consumption
- **Priority Requests**: Emergency/disabled access
- **Multi-Building Support**: Inter-building elevator networks

### Extensibility Points

- **New Scheduling Algorithms**: Implement `ElevatorSchedulingStrategy`
- **Additional States**: Extend `ElevatorState` hierarchy
- **Custom Observers**: Implement `ElevatorObserver`
- **Request Types**: Extend `Request` model

## 📚 Learning Outcomes

This project demonstrates:

1. **Advanced OOP Concepts**: Inheritance, polymorphism, encapsulation
2. **Design Pattern Implementation**: State, Strategy, Observer, Singleton
3. **System Design**: Scalable, maintainable architecture
4. **Concurrent Programming**: Thread-safe operations
5. **Real-world Problem Solving**: Elevator control system design

## 🤝 Contributing

This is an educational project demonstrating LLD principles. Feel free to:

- Add new scheduling algorithms
- Implement additional elevator features
- Improve the demo scenarios
- Add unit tests

## 📄 License

This project is for educational purposes and demonstrates Low-Level Design principles for software engineering interviews and learning.

---

**Built with ❤️ using Python and advanced design patterns**
