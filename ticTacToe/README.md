# Tic-Tac-Toe Game System

A comprehensive Low-Level Design (LLD) implementation of a tic-tac-toe game system using Python, demonstrating advanced object-oriented design principles, design patterns, and concurrent programming techniques.

## 🏗️ System Architecture

This tic-tac-toe system implements a robust, scalable architecture using multiple design patterns:

### Core Design Patterns Used

1. **State Pattern** - Manages game states (NotStarted, InProgress, Completed)
2. **Observer Pattern** - Notifies players about game status changes
3. **Strategy Pattern** - Implements different win detection algorithms
4. **Factory Pattern** - Creates players and game components

### Key Components

```
app/
├── models/           # Core domain entities
│   ├── player.py     # Human and Computer players
│   ├── board.py      # Game board with move validation
│   ├── game.py       # Game entity with win detection
│   └── enums.py      # Game status and symbol enumerations
├── states/           # State pattern implementation
│   └── game_state.py # NotStarted, InProgress, Completed states
└── observers/        # Observer pattern implementation
    └── game_observer.py # Subject/Observer base classes
```

## 🎮 Game Features

### Game States

- **NotStarted State**: Game initialization and setup
- **InProgress State**: Active gameplay with move validation
- **Completed State**: Game over with winner determination

### Player Types

- **Human Player**: Interactive input-based moves
- **Computer Player**: Automated random move selection

### Board Configurations

- **Standard 3x3**: Classic tic-tac-toe (3 in a row to win)
- **Custom Sizes**: Support for NxN boards
- **Flexible Win Conditions**: K consecutive symbols to win (K ≤ N)

## 🚀 Quick Start

### Basic Usage

```python
from tic_tac_toe_game import TicTacToeGame

# Create a game
game = TicTacToeGame(board_size=3, consecutive_moves_to_win=3)

# Play human vs computer
game.play_game(
    player1_type="human",
    player2_type="computer",
    player1_name="Human Player",
    player2_name="AI Assistant"
)
```

### Programmatic Control

```python
# Initialize players
game.initialize_players("Alice", "Bob", "human", "computer")

# Start game
game.start_game()

# Make moves
game.make_move(0, 0)  # Human player move
game.make_move()      # Computer player move (automatic)

# Check game status
if game.is_game_over():
    winner = game.get_winner()
    if winner:
        print(f"{winner.get_name()} wins!")
    else:
        print("It's a draw!")
```

## 📊 Entity Relationship Diagram

### Core Entities and Relationships

```
┌─────────────────────────────────────┐
│      TicTacToeGame                  │
│─────────────────────────────────────│
│ - board_size                        │
│ - consecutive_moves_to_win          │
│ - game (Game)                       │
│ - players (List<Player>)            │
└──────┬──────────────────────────────┘
       │
       │ 1 (has)
       │
       ▼
┌─────────────────────────────────────┐
│            Game                     │
│─────────────────────────────────────│
│ id                                  │
│ players (List<Player>)              │
│ board (Board)                       │
│ status (GameStatus)                 │
│ state (GameState)                   │
│ current_player_index                │
│ winner (Player)                     │
│ consecutive_moves_to_win            │
│ observers (List<Observer>)          │
└──────┬──────────────────────────────┘
       │
       │ references
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Board     │ │   Player    │ │  GameState  │
└─────────────┘ └─────────────┘ └─────────────┘

┌─────────────────────────────────────┐
│            Board                    │
│─────────────────────────────────────│
│ board (2D List)                     │
│ size                                │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│            Player                   │
│─────────────────────────────────────│
│ id                                  │
│ name                                │
│ symbol (PlayerSymbol)               │
│ type (PlayerType)                    │
└──────┬───────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┐
       ▼              ▼
┌─────────────┐ ┌─────────────┐
│ HumanPlayer │ │ComputerPlayer│
└─────────────┘ └─────────────┘

┌─────────────────────────────────────┐
│        GameState                    │
│─────────────────────────────────────│
│ (Abstract)                          │
└──────┬──────────────────────────────┘
       │
       │ Inheritance
       │
       ├──────────────┬──────────────┬
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ NotStarted  │ │ InProgress  │ │  Completed  │
│   State     │ │   State     │ │   State     │
└─────────────┘ └─────────────┘ └─────────────┘
```

### Entity Relationships

1. **TicTacToeGame ↔ Game** (One-to-One)

   - Game controller has one Game instance
   - Game manages the actual gameplay

2. **Game ↔ Board** (One-to-One)

   - Each Game has one Board
   - Board stores the game state

3. **Game ↔ Player** (One-to-Many)

   - A Game has multiple Players (typically 2)
   - Each Player can play in multiple Games

4. **Game ↔ GameState** (One-to-One)

   - Each Game has one current State
   - State transitions: NotStarted → InProgress → Completed

5. **Player Inheritance Hierarchy**

   - `Player` (base class)
   - `HumanPlayer`, `ComputerPlayer` (subclasses)

6. **Observer Pattern Relationships**

   - Game implements `GameSubject` - notifies on status changes
   - Player implements `GameObserver` - receives game notifications

7. **Board Structure**
   - 2D list representation
   - Cells contain PlayerSymbol (X, O, or empty)

## 🔄 Data Flow Diagrams

### 1. Game Initialization Flow

```
┌──────────┐
│   User   │
└────┬─────┘
     │
     │ 1. initialize_players()
     │ 2. initialize_game()
     ▼
┌─────────────────┐
│ TicTacToeGame   │
└────┬────────────┘
     │
     │ 3. Create Board
     │ 4. Create Players
     │ 5. Create Game
     │ 6. Set state to NotStarted
     ▼
┌─────────────────┐
│     Game        │
│  - Board        │
│  - Players      │
│  - State        │
└─────────────────┘
```

### 2. Move Execution Flow

```
┌──────────┐
│  Player  │
└────┬─────┘
     │
     │ 1. make_move(row, col)
     ▼
┌─────────────────┐
│ TicTacToeGame   │
└────┬────────────┘
     │
     │ 2. game.make_move()
     ▼
┌─────────────────┐
│     Game        │
└────┬────────────┘
     │
     │ 3. state.make_move()
     │ 4. Validate move
     │ 5. Update board
     ▼
┌─────────────────┐
│     Board       │
└────┬────────────┘
     │
     │ 6. Check win condition
     │ 7. Switch player
     │ 8. notify_observers()
     ▼
┌─────────────────┐
│   Observers     │
│  (Notified)     │
└─────────────────┘
```

### 3. Win Detection Flow

```
┌──────────┐
│   Game   │
└────┬─────┘
     │
     │ 1. After move, check_winner()
     ▼
┌─────────────────┐
│     Board       │
└────┬────────────┘
     │
     │ 2. Check horizontal
     │ 3. Check vertical
     │ 4. Check diagonal
     │ 5. Check anti-diagonal
     ▼
┌─────────────────┐
│  Win Detection  │
└────┬────────────┘
     │
     │ 6. If winner found
     │ 7. Set winner
     │ 8. Set state to Completed
     │ 9. notify_observers()
     ▼
┌─────────────────┐
│   Observers     │
│  (Notified)     │
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
│      TicTacToeGame                  │
│  - Game Initialization              │
│  - Move Management                  │
│  - Win Detection                    │
└──────┬──────────────────────────────┘
       │
       │
       ▼
┌─────────────────────────────────────┐
│            Game                     │
│  - Board Management                 │
│  - Player Management                │
│  - State Management                 │
└──────┬──────────────────────────────┘
       │
       ├──────────────────┬──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐  ┌─────────────┐  ┌──────────────┐
│   Board     │  │   Players   │  │  GameState   │
│  - Cells    │  │  - Human    │  │  - NotStarted│
│  - State    │  │  - Computer │  │  - InProgress│
│             │  │             │  │  - Completed │
└─────────────┘  └─────────────┘  └──────────────┘
       │
       │
       ▼
┌─────────────────────────────────────┐
│         Pattern Layer               │
│  - GameState (State)                │
│  - GameObserver (Observer)          │
└─────────────────────────────────────┘
```

## 📋 Entity Attributes Summary

### Game Entity

- `id`: Unique identifier (UUID)
- `players`: List of Player objects
- `board`: Reference to Board
- `status`: GameStatus (NOT_STARTED, IN_PROGRESS, COMPLETED)
- `state`: GameState object
- `current_player_index`: Index of current player
- `winner`: Winning Player (if game completed)
- `consecutive_moves_to_win`: Number of consecutive moves needed to win
- `observers`: List of Observer objects

### Board Entity

- `board`: 2D list representing game board
- `size`: Board dimensions (NxN)

### Player Entity

- `id`: Unique identifier (UUID)
- `name`: Player name
- `symbol`: PlayerSymbol (X or O)
- `type`: PlayerType (HUMAN or COMPUTER)

### HumanPlayer Entity (extends Player)

- Inherits all Player attributes
- Makes moves based on user input

### ComputerPlayer Entity (extends Player)

- Inherits all Player attributes
- Makes random moves automatically

## 🎯 Design Principles Applied

### SOLID Principles

- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Easy to add new game states and player types
- **Liskov Substitution**: All state implementations are interchangeable
- **Interface Segregation**: Clean, focused interfaces
- **Dependency Inversion**: High-level modules depend on abstractions

### Additional Principles

- **DRY (Don't Repeat Yourself)**: Reusable components
- **KISS (Keep It Simple, Stupid)**: Clear, understandable code
- **YAGNI (You Aren't Gonna Need It)**: Only implemented required features

## 📊 Game Behavior

### Win Detection Algorithm

The system implements a comprehensive win detection algorithm that checks:

1. **Horizontal Wins**: Consecutive symbols in rows
2. **Vertical Wins**: Consecutive symbols in columns
3. **Diagonal Wins**: Consecutive symbols in main diagonals
4. **Anti-Diagonal Wins**: Consecutive symbols in anti-diagonals

### State Transitions

```
NotStarted State
    ↓ (start())
InProgress State
    ↓ (win/draw condition met)
Completed State
```

### Move Validation

- **Boundary Checks**: Row/column within board limits
- **Occupancy Checks**: Cell must be empty
- **State Validation**: Moves only allowed in InProgress state

## 🧪 Demo Scenarios

The system includes comprehensive demos showcasing:

1. **Human vs Computer**: Interactive gameplay experience
2. **Computer vs Computer**: Automated gameplay demonstration
3. **Large Board (4-in-a-row)**: 5x5 board with 4 consecutive symbols to win
4. **Large Board (3-in-a-row)**: 5x5 board with 3 consecutive symbols to win
5. **Manual Control**: Programmatic game control
6. **State Transitions**: State pattern demonstration
7. **Observer Pattern**: Player notification system
8. **Error Handling**: Invalid moves and edge cases

### Running Demos

```bash
cd low_level_design/ticTacToe
python3 demo.py
```

## 🎯 Implementation Details

### State Pattern Usage

```python
# Game state management
game.set_state(NotStartedState())    # Initial state
game.start()                         # Transitions to InProgressState
# Game logic handled by current state
game.end()                          # Transitions to CompletedState
```

### Observer Pattern Implementation

```python
# Players observe game status changes
game.add_observer(player1)
game.add_observer(player2)

# Game status changes notify all observers
game.set_status(GameStatus.IN_PROGRESS)  # All players notified
```

### Win Detection Strategy

```python
# Comprehensive win checking for all directions
def check_winner(self, player: Player, row: int, col: int) -> bool:
    # Check horizontal, vertical, diagonal, and anti-diagonal
    return (self._check_horizontal(player, row) or
            self._check_vertical(player, col) or
            self._check_diagonal(player, row, col) or
            self._check_anti_diagonal(player, row, col))
```

## 🔧 Configuration Options

### Board Sizes

```python
# Standard 3x3
game = TicTacToeGame(board_size=3, consecutive_moves_to_win=3)

# Large 5x5 board with 4-in-a-row
game = TicTacToeGame(board_size=5, consecutive_moves_to_win=4)

# Large 5x5 board with 3-in-a-row (easier to win)
game = TicTacToeGame(board_size=5, consecutive_moves_to_win=3)

# Custom configurations
game = TicTacToeGame(board_size=4, consecutive_moves_to_win=3)
```

### Player Configurations

```python
# Different player combinations
game.initialize_players("Alice", "Bob", "human", "human")
game.initialize_players("Human", "AI", "human", "computer")
game.initialize_players("AI1", "AI2", "computer", "computer")
```

## 📈 Performance Characteristics

### Time Complexity

- **Move Validation**: O(1) - Simple boundary and occupancy checks
- **Win Detection**: O(N) - Linear scan of affected row/column/diagonal
- **Board Display**: O(N²) - Full board iteration

### Space Complexity

- **Board Storage**: O(N²) - 2D list for board state
- **Win Detection**: O(1) - No additional space beyond board

## 🚀 Future Enhancements

### Potential Improvements

- **AI Strategies**: Minimax algorithm for intelligent computer players
- **Network Play**: Multiplayer support over network
- **Game Persistence**: Save/load game state
- **Tournament Mode**: Multiple rounds with scoring
- **Custom Rules**: Different win conditions and board shapes

### Extensibility Points

- **New Game States**: Extend `GameState` hierarchy
- **New Player Types**: Implement custom player strategies
- **New Win Conditions**: Extend win detection algorithms
- **New Board Types**: Support hexagonal, circular boards

## 📚 Learning Outcomes

This project demonstrates:

1. **Advanced OOP Concepts**: Inheritance, polymorphism, encapsulation
2. **Design Pattern Implementation**: State, Observer, Strategy patterns
3. **System Design**: Clean architecture with separation of concerns
4. **Game Development**: Turn-based game logic and state management
5. **Error Handling**: Robust input validation and edge case handling

## 🤝 Contributing

This is an educational project demonstrating LLD principles. Feel free to:

- Add new AI strategies for computer players
- Implement network multiplayer functionality
- Add new board types and win conditions
- Improve the demo scenarios
- Add comprehensive unit tests

## 📄 License

This project is for educational purposes and demonstrates Low-Level Design principles for software engineering interviews and learning.

---

**Built with ❤️ using Python, advanced design patterns, and clean architecture principles**
