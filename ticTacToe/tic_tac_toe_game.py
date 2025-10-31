"""
Tic-Tac-Toe Game - Main Game Controller
Implements a comprehensive tic-tac-toe game with state pattern, observer pattern, and strategy pattern.
"""

from app.models.player import HumanPlayer, ComputerPlayer
from app.models.board import Board
from app.models.enums import PlayerSymbol, GameStatus, PlayerType
from app.models.game import Game
import random


class TicTacToeGame:
    """
    Main Tic-Tac-Toe Game Controller
    Handles game initialization, player management, and game flow
    """

    def __init__(self, board_size: int = 3, consecutive_moves_to_win: int = 3):
        self.board_size = board_size
        self.consecutive_moves_to_win = consecutive_moves_to_win
        self.game: Game = None
        self.players = []

    def initialize_players(
        self,
        player1_name: str = "Player 1",
        player2_name: str = "Player 2",
        player1_type: PlayerType = PlayerType.HUMAN,
        player2_type: PlayerType = PlayerType.HUMAN,
    ):
        """
        Initialize players for the game

        Args:
            player1_name: Name of first player
            player2_name: Name of second player
            player1_type: Type of first player (PlayerType.HUMAN or PlayerType.COMPUTER)
            player2_type: Type of second player (PlayerType.HUMAN or PlayerType.COMPUTER)
        """
        symbols = [PlayerSymbol.X, PlayerSymbol.O]
        random.shuffle(symbols)

        # Create first player
        if player1_type == PlayerType.COMPUTER:
            player1 = ComputerPlayer(player1_name, symbols[0])
        else:
            player1 = HumanPlayer(player1_name, symbols[0])

        # Create second player
        if player2_type == PlayerType.COMPUTER:
            player2 = ComputerPlayer(player2_name, symbols[1])
        else:
            player2 = HumanPlayer(player2_name, symbols[1])

        self.players = [player1, player2]

    def initialize_game(self):
        """Initialize a new game with current players"""
        if not self.players:
            raise ValueError("Players not initialized. Call initialize_players() first.")

        board = Board(self.board_size)
        self.game = Game(self.players, board, self.consecutive_moves_to_win)

        # Add players as observers
        for player in self.players:
            self.game.add_observer(player)

    def start_game(self):
        """Start the game"""
        if not self.game:
            self.initialize_game()

        print("🎮 Starting Tic-Tac-Toe Game!")
        print(f"Board size: {self.board_size}x{self.board_size}")
        print(f"Consecutive moves to win: {self.consecutive_moves_to_win}")
        print(f"Players: {[f'{p.get_name()} ({p.get_symbol().value})' for p in self.players]}")
        print()

        self.game.start()
        self.display_board()

    def display_board(self):
        """Display the current game board"""
        if not self.game:
            return

        board_data = self.game.get_board().get_board()
        print("Current Board:")
        print("  " + " ".join(str(i) for i in range(self.board_size)))

        for i in range(self.board_size):
            row_str = f"{i} "
            for j in range(self.board_size):
                cell = board_data[i][j]
                if cell == "-":
                    row_str += ". "
                else:
                    row_str += cell + " "
            print(row_str.rstrip())
        print()

    def make_move(self, row: int = None, col: int = None, force_move: bool = False):
        """
        Make a move in the game

        Args:
            row: Row for the move
            col: Column for the move
            force_move: If True, use provided coordinates even for computer players
        """
        if not self.game:
            raise ValueError("Game not initialized. Call start_game() first.")

        current_player = self.game.get_current_player()

        # If computer player and no coordinates provided (or force_move is False), generate random move
        if current_player.get_type() == PlayerType.COMPUTER and (row is None or col is None) and not force_move:
            available_cells = self.game.get_board().get_random_available_cell()
            if available_cells:
                row, col = available_cells
                print(f"🤖 {current_player.get_name()} plays at ({row}, {col})")
        else:
            # For human players or when coordinates are explicitly provided
            if row is None or col is None:
                raise ValueError("Row and column must be provided for human players or when forcing moves")

        # Make the move using the game state
        try:
            self.game.get_state().make_move(self.game, current_player, row, col)

            # Switch to next player
            self.game.current_player_index = (self.game.current_player_index + 1) % len(self.players)

            self.display_board()

        except ValueError as e:
            return False

        return True

    def is_game_over(self) -> bool:
        """Check if the game is over"""
        if not self.game:
            return False
        return self.game.get_status() == GameStatus.COMPLETED

    def get_winner(self):
        """Get the winner of the game"""
        if not self.game:
            return None
        return self.game.get_winner()

    def get_current_player(self):
        """Get the current player"""
        if not self.game:
            return None
        return self.game.get_current_player()

    def end_game(self):
        """End the current game"""
        if self.game:
            self.game.end()

    def play_game(
        self,
        player1_type: PlayerType = PlayerType.HUMAN,
        player2_type: PlayerType = PlayerType.COMPUTER,
        player1_name: str = "Human",
        player2_name: str = "Computer",
    ):
        """
        Play a complete game with automatic move handling

        Args:
            player1_type: Type of player 1 (PlayerType.HUMAN or PlayerType.COMPUTER)
            player2_type: Type of player 2 (PlayerType.HUMAN or PlayerType.COMPUTER)
            player1_name: Name of player 1
            player2_name: Name of player 2
        """
        # Initialize players
        self.initialize_players(player1_name, player2_name, player1_type, player2_type)

        # Start game
        self.start_game()

        # Game loop
        while not self.is_game_over():
            current_player = self.get_current_player()
            player_name = current_player.get_name()
            player_type = current_player.get_type()

            if player_type == PlayerType.HUMAN:
                # For human players, get input
                while True:
                    try:
                        row = int(input(f"{player_name}, enter row (0-{self.board_size-1}): "))
                        col = int(input(f"{player_name}, enter column (0-{self.board_size-1}): "))

                        if self.make_move(row, col):
                            break
                        else:
                            print("Invalid move, try again.")
                    except ValueError:
                        print("Invalid input. Please enter numbers only.")
            else:
                # For computer players, make automatic move
                import time

                time.sleep(1)  # Add delay for computer moves
                self.make_move()

        # Game over
        winner = self.get_winner()
        if winner:
            print(f"🎉 Congratulations! {winner.get_name()} wins!")
        else:
            print("🤝 It's a draw!")


if __name__ == "__main__":
    # Example usage
    game = TicTacToeGame(board_size=3, consecutive_moves_to_win=3)
    game.play_game()
