# 🏏 CricInfo - Cricket Management System

A comprehensive cricket management system built with Python that demonstrates advanced software design patterns and real-time cricket match simulation.

## 📋 Features

### Core Functionality

- **Player & Team Management**: Create and manage cricket players and teams
- **Match Scheduling**: Schedule matches with different formats (T20, ODI, TEST)
- **Live Match Simulation**: Real-time ball-by-ball match simulation
- **Search Functionality**: Search for matches, players, and teams
- **Match History**: View completed matches and results
- **Real-time Updates**: Live scorecard, commentary, and notifications

### Advanced Features

- **Concurrent Access**: Thread-safe operations with ThreadPoolExecutor
- **Scalable Architecture**: Service-oriented design with proper separation of concerns
- **Extensible Design**: Built with multiple design patterns for easy extension

## 🏗️ Architecture & Design Patterns

### Design Patterns Implemented

- **Singleton Pattern**: `CricInfoService` for centralized access
- **Observer Pattern**: Real-time updates (ScorecardDisplay, CommentaryManager, UserNotifier)
- **Builder Pattern**: Complex object creation (BallBuilder, WicketBuilder)
- **State Pattern**: Match progression (ScheduledState, LiveState, FinishedState)
- **Facade Pattern**: `CricInfoService` orchestrating other services

### Project Structure

```
cricinfo/
├── app/
│   ├── builders/          # Builder pattern implementations
│   │   ├── ball_builder.py
│   │   └── wicket_builder.py
│   ├── models/            # Core domain models
│   │   ├── ball.py
│   │   ├── inning.py
│   │   ├── match.py
│   │   ├── player.py
│   │   ├── player_stats.py
│   │   ├── team.py
│   │   └── wicket.py
│   ├── observers/         # Observer pattern implementations
│   │   └── match_observer.py
│   ├── services/          # Business logic services
│   │   ├── cric_info_service.py
│   │   ├── match_service.py
│   │   ├── player_service.py
│   │   └── commentary_service.py
│   ├── states/            # State pattern implementations
│   │   └── match_state.py
│   └── models/
│       └── enums.py       # Enumeration definitions
├── run.py                 # Main demo script
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. **Clone or navigate to the project directory**

   ```bash
   cd /path/to/cricinfo
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies** (if any)

   ```bash
   pip install -r requirements.txt  # If requirements.txt exists
   ```

4. **Run the demo**
   ```bash
   python run.py
   ```

## 🎯 Usage

### Running the Demo

The `run.py` script demonstrates all system features:

```bash
python run.py
```

### Demo Sections

1. **Player & Team Management**: Creates teams and players
2. **Match Scheduling**: Schedules multiple matches
3. **Search Functionality**: Demonstrates various search operations
4. **Live Match Simulation**: Complete match with commentary
5. **Concurrent Access**: ThreadPoolExecutor demonstration
6. **Match History**: Shows completed and upcoming matches
7. **Detailed Statistics**: Player and match statistics
8. **Scalability Test**: Multiple match creation
9. **Real-time Updates**: Observer pattern demonstration

### Sample Output

```
🏏 Welcome to CricInfo Demo - Complete Cricket Management System
================================================================================

📋 1. PLAYER AND TEAM MANAGEMENT
----------------------------------------
✅ Created team: India
✅ Created team: Australia
✅ Created team: England
✅ Created team: Pakistan

📅 2. MATCH SCHEDULING
----------------------------------------
✅ Scheduled: India vs Australia (T20)
✅ Scheduled: England vs Pakistan (ODI)
✅ Scheduled: India vs England (TEST)

🔍 3. SEARCH FUNCTIONALITY
----------------------------------------
Searching for matches involving India:
   Found: India vs Australia
   Found: India vs England
...
```

## 🔧 API Usage

### Basic Operations

#### Creating Players and Teams

```python
from app.services.cric_info_service import CricInfoService
from app.models.enums import PlayerRole, MatchType
from app.models.team import Team

service = CricInfoService.get_instance()

# Create players
virat = service.add_player("Virat Kohli", "India", PlayerRole.BATSMAN)
rohit = service.add_player("Rohit Sharma", "India", PlayerRole.BATSMAN)

# Create team
india = Team("India", [virat, rohit])
```

#### Creating and Managing Matches

```python
# Create match
match = service.create_match(india, australia, MatchType.T20)

# Start match
service.start_match(match.get_id())

# Process ball
from app.builders.ball_builder import BallBuilder
ball = BallBuilder().with_ball_number(1).with_bowled_by(bowler).with_faced_by(batsman).with_runs_scored(4).build()
service.process_ball(match.get_id(), ball)
```

#### Search Operations

```python
# Search matches by team
matches = service.search_matches_by_team("India")

# Search players by name
players = service.search_players_by_name("Virat")

# Search players by country
indian_players = service.search_players_by_country("India")
```

#### Getting Match Information

```python
# Get match details
match_details = service.get_match_details(match_id)

# Get player statistics
player_stats = service.get_player_details(player_id)

# Get match history
all_matches = service.get_match_history()
finished_matches = service.get_finished_matches()
```

## 🧪 Testing

### Running Tests

```bash
# Run the comprehensive demo
python run.py

# The demo includes:
# - Player and team creation
# - Match simulation
# - Search functionality
# - Concurrent access testing
# - Statistics display
```

### Test Coverage

The demo script tests:

- ✅ Player and team management
- ✅ Match creation and scheduling
- ✅ Search functionality
- ✅ Live match simulation
- ✅ Real-time updates
- ✅ Concurrent access
- ✅ Statistics and reporting

## 🔄 Concurrent Access

The system demonstrates thread-safe operations using `ThreadPoolExecutor`:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = []
    for team in ["India", "Australia", "England", "Pakistan"]:
        future = executor.submit(access_match, match_id, team)
        futures.append(future)

    for future in as_completed(futures):
        result = future.result()
        print(f"✅ {result}")
```

## 📊 Performance & Scalability

### Features

- **Thread-safe operations**: All services use proper locking mechanisms
- **Efficient search**: Optimized search algorithms for players and matches
- **Memory management**: Proper object lifecycle management
- **Scalable architecture**: Service-oriented design supports horizontal scaling

### Benchmarks

- Supports multiple concurrent matches
- Handles thousands of players and teams
- Real-time updates with minimal latency
- Efficient memory usage with proper cleanup

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for public methods
- Maintain test coverage

## 📝 License

This project is for educational purposes and demonstrates software design patterns in Python.

## 🎓 Learning Objectives

This project demonstrates:

- **Object-Oriented Programming**: Classes, inheritance, polymorphism
- **Design Patterns**: Singleton, Observer, Builder, State, Facade
- **Concurrency**: Thread-safe operations, ThreadPoolExecutor
- **Software Architecture**: Service-oriented design, separation of concerns
- **Real-time Systems**: Observer pattern for live updates
- **Data Management**: Efficient search and retrieval operations

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**

   ```bash
   # Ensure you're in the correct directory
   cd /path/to/cricinfo

   # Check Python path
   python -c "import sys; print(sys.path)"
   ```

2. **Virtual Environment Issues**

   ```bash
   # Recreate virtual environment
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   ```

3. **Permission Issues**
   ```bash
   # Make script executable
   chmod +x run.py
   ```

## 📞 Support

For questions or issues:

1. Check the troubleshooting section
2. Review the demo output for error messages
3. Ensure all dependencies are installed
4. Verify Python version compatibility

## 🏆 Acknowledgments

This project demonstrates advanced software engineering concepts and design patterns commonly used in production systems. It serves as an excellent learning resource for understanding how to build scalable, maintainable software systems.

---

**Happy Coding! 🏏**
