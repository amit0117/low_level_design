# 🐍 Snake and Ladder Game - Low Level Design Implementation

A comprehensive implementation of the classic Snake and Ladder game showcasing various design patterns, concurrency concepts, and object-oriented programming principles.

## 🎯 Overview

This project demonstrates a robust, multi-threaded Snake and Ladder game implementation with:

- **Multiple concurrent games** running simultaneously
- **Observer pattern** for real-time game notifications
- **State management** with pause/resume functionality
- **Thread-safe operations** using ThreadPoolExecutor
- **Dynamic board configuration** with customizable sizes

## 🏗️ Architecture & Design Patterns

### Design Patterns Implemented

1. **Singleton Pattern** - Single game system instance
2. **State Pattern** - Game state management (NOT_STARTED → RUNNING → FINISHED)
3. **Observer Pattern** - Automatic player notifications for game events
4. **Factory Pattern** - Board and player creation
5. **Strategy Pattern** - Dice rolling mechanics
6. **Concurrency Pattern** - ThreadPoolExecutor for multiple concurrent games

### Project Structure

```
SnakeAndLadderGame/
├── app/
│   ├── models/
│   │   ├── board.py          # Board representation with snakes and ladders
│   │   ├── cell.py           # Individual cell on the board
│   │   ├── dice.py           # Dice rolling logic
│   │   ├── enums.py          # Game status enumerations
│   │   ├── game.py           # Main game logic and state management
│   │   └── player.py         # Player model with observer capabilities
│   ├── observers/
│   │   └── game_observer.py  # Observer pattern implementation
│   ├── services/
│   │   ├── board_service.py # Board creation and management
│   │   ├── game_service.py   # Game creation and management
│   │   └── player_service.py # Player management
│   └── state/
│       └── game_state.py     # State pattern implementation
├── snake_and_ladder_game.py  # Main game system (Singleton)
├── run.py                    # Demo application with multiple scenarios
└── README.md                 # This file
```

## 🚀 Features

### Core Game Features

- **Multi-player support** (2+ players per game)
- **Snakes and Ladders** with predefined positions
- **Dice rolling** with consecutive turn logic (roll 6 = extra turn)
- **Win condition** - land exactly on the final position
- **Dynamic board sizes** - customizable board dimensions

### Advanced Features

- **Concurrent game execution** using ThreadPoolExecutor
- **Real-time notifications** via Observer pattern
- **Game state management** (pause/resume functionality)
- **Thread-safe operations** for multi-threaded environments
- **Comprehensive error handling** and edge case management

### Demo Scenarios

1. **Single Game Session** - Basic 3-player game
2. **Multiple Concurrent Games** - 4 games running simultaneously
3. **Edge Cases** - Single player validation, large player counts
4. **Observer Pattern** - Real-time game notifications

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7+
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd SnakeAndLadderGame
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Run the demo**
   ```bash
   python run.py
   ```

## 🎮 How to Play

### Basic Rules

1. **Objective**: Be the first player to reach the final position (exactly)
2. **Movement**: Roll dice and move forward by the number shown
3. **Snakes**: If you land on a snake's head, slide down to its tail
4. **Ladders**: If you land on a ladder's bottom, climb up to its top
5. **Extra Turns**: Rolling a 6 gives you an additional turn (max 3 consecutive)
6. **Winning**: Land exactly on the final position to win

### Game Flow

1. Players take turns rolling the dice
2. Move forward by the dice value
3. Handle snakes/ladders if encountered
4. Continue until someone reaches the final position
5. Game ends and winner is declared

## 🔧 Configuration

### Board Setup

The game supports dynamic board configuration:

```python
# Create a game with custom board size
game = game_system.create_new_game(["Player1", "Player2"], board_size=50)
```

### Snakes and Ladders

Predefined snakes and ladders are automatically placed based on board size:

- **Snakes**: (17→7), (54→34), (62→19), (98→79)
- **Ladders**: (3→38), (24→33), (42→93), (72→84)

Only snakes/ladders that fit within the board size are placed.

## 📊 Demo Output Example

```
🐍 Snake and Ladder Game Demo - Design Patterns & Concurrency Showcase
======================================================================

📋 Demo 1: Single Game Session
--------------------------------------------------
🎮 Starting single game with 3 players...
🎲 Board setup complete with 1 snakes and 0 ladders
✅ Game created with ID: 834a7045...
👥 Players: ['Alice', 'Bob', 'Charlie']
🎯 Game Status: NOT_STARTED

🎲 Single Game starting...
Alice rolled a 5
Alice moved from 0 to 5
Bob rolled a 3
Bob moved from 0 to 3
Charlie rolled a 1
Charlie moved from 0 to 1
...
Alice moved from 18 to 19
Game with id 834a7045... status changed from running to finished
You are the winner of the game with id 834a7045...
```

## 🧪 Testing & Validation

### Edge Cases Handled

- **Single player games** - Rejected with appropriate error message
- **Large player counts** - Supports up to 10+ players
- **Invalid moves** - Players skip turns when they can't move
- **Concurrent games** - Multiple games run simultaneously without conflicts

### Thread Safety

- All game operations are thread-safe
- ThreadPoolExecutor manages concurrent game execution
- Observer notifications work correctly across threads

## 🔍 Key Implementation Details

### Observer Pattern

```python
# Players automatically receive notifications
class Player(GameObserver):
    def update(self, game):
        if game.get_winner():
            print(f"You are the winner!")
        else:
            print(f"Game status: {game.get_status()}")
```

### State Management

```python
# Game states: NOT_STARTED → RUNNING → FINISHED
class RunningState(GameState):
    def stop(self, game):
        game.setStatus(GameStatus.FINISHED)
        game.setState(FinishedState())
```

### Concurrency

```python
# Multiple games run concurrently
with ThreadPoolExecutor(max_workers=4) as executor:
    for game in games:
        executor.submit(self._play_game, game)
```

## 🎯 Design Decisions

### Why These Patterns?

- **Singleton**: Ensures single game system instance
- **State**: Clean separation of game states and transitions
- **Observer**: Decoupled notification system for game events
- **Factory**: Centralized object creation with validation
- **Strategy**: Flexible dice rolling implementation
- **ThreadPoolExecutor**: Efficient resource management for concurrent games

### Thread Safety Considerations

- All shared resources are properly synchronized
- Game state changes are atomic
- Observer notifications are thread-safe
- No race conditions in concurrent game execution

## 🚀 Future Enhancements

### Potential Improvements

- **GUI Interface** - Visual game board and player interactions
- **Network Multiplayer** - Remote players over network
- **Game Statistics** - Win/loss tracking and analytics
- **Custom Boards** - User-defined snake and ladder positions
- **Tournament Mode** - Multiple rounds with scoring
- **AI Players** - Computer-controlled opponents

### Performance Optimizations

- **Database Integration** - Persistent game state storage
- **Caching** - Board state and player position caching
- **Load Balancing** - Distributed game execution
- **Metrics Collection** - Performance monitoring and analytics

## 📝 License

This project is for educational purposes and demonstrates various design patterns and concurrency concepts in Python.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📞 Contact

For questions or suggestions, please open an issue in the repository.

---

**Happy Gaming! 🎲🐍**
