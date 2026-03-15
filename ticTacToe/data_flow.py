"""
Mermaid Diagrams for Tic-Tac-Toe - Low Level Design
"""

DATA_FLOW_DIAGRAM = """
```mermaid
graph TD
    TicTacToeGame[TicTacToeGame] -->|creates| Game[Game Subject]
    Game -->|has| Board[Board]
    Board -->|grid of| Cells[Cells NxN]

    Game -->|has| Players{Players}
    Players -->|human| HumanPlayer[HumanPlayer]
    Players -->|computer| ComputerPlayer[ComputerPlayer]

    HumanPlayer -->|has| Symbol1[PlayerSymbol X/O]
    ComputerPlayer -->|has| Symbol2[PlayerSymbol X/O]
    ComputerPlayer -->|uses| Minimax[Minimax Algorithm]

    Game -->|has| GameState{Game State}
    GameState -->|not started| NotStartedState[NotStartedState]
    GameState -->|in progress| InProgressState[InProgressState]
    GameState -->|completed| CompletedState[CompletedState]

    Game -->|has| GameStatus[GameStatus]
    Game -->|observed by| GameObserver[GameObserver]
    GameObserver -->|notifies| Players
```
"""

USER_FLOW_DIAGRAM = """
```mermaid
sequenceDiagram
    actor Player1 as Player 1 (Human - X)
    actor Player2 as Player 2 (Human/Computer - O)
    participant TicTacToe as TicTacToeGame
    participant Game
    participant Board
    participant GameObserver

    TicTacToe->>Game: Initialize game
    Game->>Board: Create NxN board
    Note over Game: State = NotStartedState

    TicTacToe->>Game: Start game
    Note over Game: State = InProgressState

    loop Until win or draw
        Game->>Player1: Your turn (X)
        Player1->>Board: Place X at (row, col)
        Board->>Game: Cell updated

        Game->>Game: Check win condition
        alt Player 1 wins
            Note over Game: State = CompletedState
            Game->>GameObserver: Player 1 wins!
            GameObserver-->>Player1: You win!
            GameObserver-->>Player2: You lose!
        else Board full (Draw)
            Note over Game: State = CompletedState
            Game->>GameObserver: Game is a draw!
        else Game continues
            Game->>Player2: Your turn (O)

            alt Human Player
                Player2->>Board: Place O at (row, col)
            else Computer Player
                Player2->>Player2: Run Minimax algorithm
                Player2->>Board: Place O at optimal position
            end

            Board->>Game: Cell updated
            Game->>Game: Check win condition

            alt Player 2 wins
                Note over Game: State = CompletedState
                Game->>GameObserver: Player 2 wins!
            else Game continues
                Note over Game: Next round
            end
        end
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
