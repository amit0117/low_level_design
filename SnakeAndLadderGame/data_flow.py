"""
Mermaid Diagrams for Snake and Ladder Game - Low Level Design
"""

DATA_FLOW_DIAGRAM = """
```mermaid
graph TD
    SnakeAndLadderGame[SnakeAndLadderGame] -->|creates| Game[Game]
    Game -->|has| Board[Board]
    Game -->|has| Players[Players]
    Game -->|has| GameState{Game State}

    GameState -->|not started| NotStartedState[NotStartedState]
    GameState -->|running| RunningState[RunningState]
    GameState -->|paused| PausedState[PausedState]
    GameState -->|finished| FinishedState[FinishedState]

    Board -->|managed by| BoardService[BoardService]
    Board -->|contains| Cells[Cell Grid]
    Cells -->|may have| Snake[Snake]
    Cells -->|may have| Ladder[Ladder]
    Snake -->|moves player| SnakeDown[Down to tail]
    Ladder -->|moves player| LadderUp[Up to top]

    Players -->|managed by| PlayerService[PlayerService]
    Players -->|roll| Dice[Dice]
    Dice -->|returns| DiceValue[Dice Value]
    DiceValue -->|determines| Movement[Player Movement]
    Movement -->|lands on| Cells

    Game -->|notifies| GameObserver[GameObserver]
    GameObserver -->|updates| Players
```
"""

USER_FLOW_DIAGRAM = """
```mermaid
sequenceDiagram
    actor Player1 as Player 1
    actor Player2 as Player 2
    participant Game
    participant Board
    participant Dice
    participant BoardService
    participant GameObserver

    Player1->>Game: Join game
    Player2->>Game: Join game
    Game->>Game: Initialize board with snakes & ladders
    Note over Game: State = NotStartedState

    Game->>Game: Start game
    Note over Game: State = RunningState

    loop Until a player wins
        Game->>Player1: Your turn
        Player1->>Dice: Roll dice
        Dice-->>Game: Dice value (e.g., 4)
        Game->>BoardService: Move Player1 by 4
        BoardService->>Board: Check destination cell

        alt Snake on cell
            Board-->>BoardService: Snake found!
            BoardService->>Board: Move to snake tail
        else Ladder on cell
            Board-->>BoardService: Ladder found!
            BoardService->>Board: Move to ladder top
        else Normal cell
            Board-->>BoardService: Safe cell
        end

        Game->>GameObserver: Notify position update
        GameObserver-->>Player1: Updated position
        GameObserver-->>Player2: Updated position

        Game->>Game: Check win condition

        Note over Game: Player 2's turn (same flow)
        Game->>Player2: Your turn
        Player2->>Dice: Roll dice
        Dice-->>Game: Dice value
        Game->>BoardService: Move Player2
    end

    Note over Game: State = FinishedState
    Game->>GameObserver: Announce winner
    GameObserver-->>Player1: Game result
    GameObserver-->>Player2: Game result
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
