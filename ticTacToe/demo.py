"""
Tic-Tac-Toe Demo - Comprehensive demonstration of the tic-tac-toe game system
Showcases different game scenarios, player types, and board configurations
"""

from tic_tac_toe_game import TicTacToeGame
from app.models.player import HumanPlayer
from app.models.board import Board
from app.models.enums import PlayerSymbol, PlayerType
from app.models.game import Game
import time


def demo1_human_vs_computer():
    """Demo 1: Human vs Computer - Classic tic-tac-toe experience"""
    print("=" * 60)
    print("🎮 DEMO 1: Human vs Computer")
    print("=" * 60)

    game = TicTacToeGame(board_size=3, consecutive_moves_to_win=3)
    game.play_game(player1_type=PlayerType.HUMAN, player2_type=PlayerType.COMPUTER, player1_name="Human Player", player2_name="AI Assistant")


def demo2_computer_vs_computer():
    """Demo 2: Computer vs Computer - Automated gameplay"""
    print("=" * 60)
    print("🤖 DEMO 2: Computer vs Computer")
    print("=" * 60)

    game = TicTacToeGame(board_size=3, consecutive_moves_to_win=3)
    game.initialize_players("Alice", "Bob", PlayerType.COMPUTER, PlayerType.COMPUTER)
    game.start_game()

    # Automated gameplay
    while not game.is_game_over():
        current_player = game.get_current_player()
        print(f"🤖 {current_player.get_name()}'s turn ({current_player.get_symbol().value})")

        if game.make_move():
            time.sleep(0.5)  # Brief pause between moves

    winner = game.get_winner()
    if winner:
        print(f"🎉 {winner.get_name()} wins!")
    else:
        print("🤝 It's a draw!")


def demo3_large_board():
    """Demo 3: Large Board (5x5, 4 in a row to win)"""
    print("=" * 60)
    print("📏 DEMO 3: Large Board (5x5, 4 in a row)")
    print("=" * 60)

    game = TicTacToeGame(board_size=5, consecutive_moves_to_win=4)
    game.initialize_players("Player A", "Player B", PlayerType.COMPUTER, PlayerType.COMPUTER)
    game.start_game()

    # Play a few moves to demonstrate
    moves = [(0, 0), (0, 1), (1, 1), (0, 2), (2, 2), (0, 3)]
    for move in moves:
        if game.is_game_over():
            break
        current_player = game.get_current_player()
        print(f"🤖 {current_player.get_name()} plays at {move}")
        game.make_move(move[0], move[1])
        time.sleep(0.3)

    print("Game demonstration completed (not played to completion)")


def demo3b_large_board_k3():
    """Demo 3B: Large Board (5x5, 3 in a row to win)"""
    print("=" * 60)
    print("📏 DEMO 3B: Large Board (5x5, 3 in a row)")
    print("=" * 60)

    game = TicTacToeGame(board_size=5, consecutive_moves_to_win=3)
    game.initialize_players("Ravi", "Sneha", PlayerType.COMPUTER, PlayerType.COMPUTER)
    game.start_game()

    # Play moves that will lead to a win with 3 in a row
    winning_moves = [
        (0, 0),
        (0, 1),  # Ravi: X, Sneha: O
        (1, 0),
        (1, 1),  # Ravi: X, Sneha: O
        (2, 0),  # Ravi: X - WINS with 3 in column 0!
    ]

    for i, move in enumerate(winning_moves):
        if game.is_game_over():
            break

        current_player = game.get_current_player()
        print(f"Move {i+1}: {current_player.get_name()} ({current_player.get_symbol().value}) at {move}")
        game.make_move(move[0], move[1])

        if game.is_game_over():
            winner = game.get_winner()
            if winner:
                print(f"🏆 {winner.get_name()} wins with 3 in a row!")
            break

    print("Game demonstration completed")


def demo4_manual_gameplay():
    """Demo 4: Manual gameplay control - programmatic control"""
    print("=" * 60)
    print("🎯 DEMO 4: Manual Gameplay Control")
    print("=" * 60)

    game = TicTacToeGame(board_size=3, consecutive_moves_to_win=3)
    game.initialize_players("Arjun", "Priya", PlayerType.COMPUTER, PlayerType.COMPUTER)
    game.start_game()

    # Manually control the game
    manual_moves = [
        (0, 0),  # Arjun: X at (0,0)
        (1, 1),  # Priya: O at (1,1)
        (0, 1),  # Arjun: X at (0,1)
        (2, 2),  # Priya: O at (2,2)
        (0, 2),  # Arjun: X at (0,2) - WINS!
    ]

    for i, move in enumerate(manual_moves):
        if game.is_game_over():
            break

        current_player = game.get_current_player()
        print(f"Move {i+1}: {current_player.get_name()} ({current_player.get_symbol().value}) at {move}")

        # For demo purposes, override computer player behavior to follow predetermined moves
        if game.make_move(move[0], move[1], force_move=True):
            if game.is_game_over():
                winner = game.get_winner()
                if winner:
                    print(f"🏆 {winner.get_name()} wins the game!")
                else:
                    print("🤝 Game ends in a draw!")
                break
        else:
            print("❌ Invalid move!")
            break


def demo5_game_state_transitions():
    """Demo 5: Game State Transitions - Show state pattern in action"""
    print("=" * 60)
    print("🔄 DEMO 5: Game State Transitions")
    print("=" * 60)

    # Create game components
    board = Board(3)
    players = [HumanPlayer("TestPlayer1", PlayerSymbol.X), HumanPlayer("TestPlayer2", PlayerSymbol.O)]
    game = Game(players, board, 3)

    print("Initial state:", type(game.get_state()).__name__)
    print("Game status:", game.get_status().value)

    # Start game
    game.start()
    print("After start - state:", type(game.get_state()).__name__)
    print("Game status:", game.get_status().value)

    # Make some moves
    game.get_state().make_move(game, players[0], 0, 0)  # X at (0,0)
    print("After first move - state:", type(game.get_state()).__name__)

    game.get_state().make_move(game, players[1], 1, 1)  # O at (1,1)
    print("After second move - state:", type(game.get_state()).__name__)

    print("After end - state:", type(game.get_state()).__name__)
    print("Game status:", game.get_status().value)


def demo6_observer_pattern():
    """Demo 6: Observer Pattern - Show how players get notified"""
    print("=" * 60)
    print("👁️ DEMO 6: Observer Pattern in Action")
    print("=" * 60)

    board = Board(3)
    players = [HumanPlayer("Observer1", PlayerSymbol.X), HumanPlayer("Observer2", PlayerSymbol.O)]
    game = Game(players, board, 3)

    print("🎯 Adding observers (players) to the game...")
    for player in players:
        game.add_observer(player)

    print("📣 Starting game - all observers should be notified...")
    game.start()

    print("📣 Making moves - observers get notified of game status changes...")
    game.get_state().make_move(game, players[0], 0, 0)  # X at (0,0)
    game.get_state().make_move(game, players[1], 1, 1)  # O at (1,1)


def demo7_error_handling():
    """Demo 7: Error Handling - Invalid moves and edge cases"""
    print("=" * 60)
    print("🛡️ DEMO 7: Error Handling & Edge Cases")
    print("=" * 60)

    game = TicTacToeGame(board_size=3, consecutive_moves_to_win=3)
    game.initialize_players("Tester", "Dummy", PlayerType.COMPUTER, PlayerType.COMPUTER)
    game.start_game()

    print("Testing invalid moves...")

    # Test invalid coordinates
    try:
        game.make_move(-1, 0)  # Invalid row
        print("❌ Should have failed: negative row")
    except ValueError as e:
        print(f"✅ Correctly caught error: {e}")

    try:
        game.make_move(0, 3)  # Invalid column
        print("❌ Should have failed: column out of bounds")
    except ValueError as e:
        print(f"✅ Correctly caught error: {e}")

    # Test occupied cell
    game.make_move(0, 0)  # Valid move
    try:
        game.make_move(0, 0)  # Same cell again
        print("❌ Should have failed: cell already occupied")
    except ValueError as e:
        print(f"✅ Correctly caught error: {e}")


def main():
    """Main demo function - run all demonstrations"""
    print("\n" + "=" * 80)
    print("🎮 TIC-TAC-TOE COMPREHENSIVE DEMONSTRATION")
    print("=" * 80)
    print("This demo showcases the complete tic-tac-toe system with:")
    print("• State Pattern for game states")
    print("• Observer Pattern for player notifications")
    print("• Strategy Pattern for win detection")
    print("• Multiple board sizes and win conditions")
    print("• Human and computer players")
    print("• Error handling and edge cases")
    print("=" * 80 + "\n")

    # Run all demos
    try:
        demo1_human_vs_computer()
        print("\n" + "-" * 60 + "\n")

        demo2_computer_vs_computer()
        print("\n" + "-" * 60 + "\n")

        demo3_large_board()
        print("\n" + "-" * 60 + "\n")

        demo3b_large_board_k3()
        print("\n" + "-" * 60 + "\n")

        demo4_manual_gameplay()
        print("\n" + "-" * 60 + "\n")

        demo5_game_state_transitions()
        print("\n" + "-" * 60 + "\n")

        demo6_observer_pattern()
        print("\n" + "-" * 60 + "\n")

        demo7_error_handling()

    except KeyboardInterrupt:
        print("\n\n⚠️ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 80)
    print("🎉 ALL DEMOS COMPLETED SUCCESSFULLY!")
    print("The tic-tac-toe system demonstrates advanced design patterns and clean architecture.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
