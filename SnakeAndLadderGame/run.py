import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from snake_and_ladder_game import SnakeAndLadderGame
from app.models.enums import GameStatus


class SnakeAndLadderGameDemo:
    def __init__(self):
        self.game_system = SnakeAndLadderGame.get_instance()
        self.active_games = []

    def run(self):
        print("🐍 Snake and Ladder Game Demo - Design Patterns & Concurrency Showcase")
        print("=" * 70)

        # Demo 1: Single Game Session
        print("\n📋 Demo 1: Single Game Session")
        print("-" * 50)
        self._demo_single_game()

        # Demo 2: Multiple Concurrent Games with ThreadPoolExecutor
        print("\n📋 Demo 2: Multiple Concurrent Games (ThreadPoolExecutor)")
        print("-" * 50)
        self._demo_concurrent_games_with_executor()

        # Demo 3: Edge Cases
        print("\n📋 Demo 3: Edge Cases")
        print("-" * 50)
        self._demo_edge_cases()

        # Demo 4: Observer Pattern
        print("\n📋 Demo 4: Observer Pattern - Game Notifications")
        print("-" * 50)
        self._demo_observer_pattern()

        # Wait for all games to complete using ThreadPoolExecutor
        self._wait_for_games_completion_with_executor()

        # Summary
        self._print_summary()

    def _demo_single_game(self):
        """Demo 1: Single game session with 3 players"""
        print("🎮 Starting single game with 3 players...")

        game = self.game_system.create_new_game(["Alice", "Bob", "Charlie"], 20)
        self.active_games.append(game)

        print(f"✅ Game created with ID: {game.get_id()[:8]}...")
        print(f"👥 Players: {[player.get_name() for player in game.get_players()]}")
        print(f"🎯 Game Status: {game.get_status().value}")

        # Start the game in a separate thread
        game_thread = threading.Thread(target=self._play_game, args=(game, "Single Game"))
        game_thread.start()
        game_thread.join()  # Wait for this single game to complete

    def _demo_concurrent_games_with_executor(self):
        """Demo 2: Multiple concurrent games using ThreadPoolExecutor"""
        print("🎮 Starting multiple concurrent games with ThreadPoolExecutor...")

        # Create multiple games
        games_config = [
            (["Amit", "Kushal", "Vivek"], "Game A"),
            (["Ankush", "Bhavesh", "Aman", "Prashant"], "Game B"),
            (["Dhruv", "Ekta", "Papa", "Maa"], "Game C"),
            (["Player1", "Player2", "Player3", "Player4", "Player5"], "Game D"),
        ]

        # Use ThreadPoolExecutor for better resource management
        with ThreadPoolExecutor(max_workers=4, thread_name_prefix="GameThread") as executor:
            # Submit all games to the executor
            future_to_game = {}

            for players, game_name in games_config:
                game = self.game_system.create_new_game(players, 40)
                self.active_games.append(game)

                print(f"✅ {game_name} created with ID: {game.get_id()[:8]}...")
                print(f"👥 Players: {players}")

                # Submit game to executor
                future = executor.submit(self._play_game, game, game_name)
                future_to_game[future] = (game, game_name)

            # Process completed games as they finish
            for future in as_completed(future_to_game):
                game, game_name = future_to_game[future]
                try:
                    result = future.result()
                    print(f"🏁 {game_name} completed successfully!")
                except Exception as e:
                    print(f"❌ {game_name} failed with error: {e}")


    def _demo_edge_cases(self):
        """Demo 4: Edge cases handling"""
        print("🎮 Testing edge cases...")

        # Edge Case 1: Single player game (should fail)
        print("\n🚫 Edge Case 1: Single player game")
        try:
            single_player_game = self.game_system.create_new_game(["LonelyPlayer"], 45)
            print("❌ Single player game should not be allowed!")
        except Exception as e:
            print(f"✅ Correctly handled: {e}")

        # Edge Case 2: Large number of players
        print("\n🎯 Edge Case 2: Large number of players")
        large_player_list = [f"Player{i}" for i in range(1, 11)]  # 10 players
        large_game = self.game_system.create_new_game(large_player_list, 60)
        self.active_games.append(large_game)

        print(f"✅ Large game created with {len(large_player_list)} players")
        print(f"👥 Players: {large_player_list[:5]}... (showing first 5)")

        # Use ThreadPoolExecutor for large game
        with ThreadPoolExecutor(max_workers=1, thread_name_prefix="LargeGame") as executor:
            future = executor.submit(self._play_game, large_game, "Large Game")

            try:
                result = future.result()
                print(f"🏁 Large Game completed!")
            except Exception as e:
                print(f"❌ Large Game error: {e}")

    def _demo_observer_pattern(self):
        """Demo 5: Observer pattern for game notifications"""
        print("🎮 Starting observer pattern demo...")

        game = self.game_system.create_new_game(["Observer1", "Observer2", "Observer3"], 70)
        self.active_games.append(game)

        print(f"✅ Observer Game created - players will automatically receive notifications")

        # Use ThreadPoolExecutor for observer demo
        with ThreadPoolExecutor(max_workers=1, thread_name_prefix="ObserverGame") as executor:
            future = executor.submit(self._play_game, game, "Observer Game")

            try:
                result = future.result()
                print(f"🏁 Observer Game completed!")
            except Exception as e:
                print(f"❌ Observer Game error: {e}")

    def _play_game(self, game, game_name):
        """Play a game with proper error handling"""
        try:
            print(f"\n🎲 {game_name} starting...")
            game.play()
            return f"{game_name} completed successfully"
        except Exception as e:
            raise Exception(f"{game_name} failed: {e}")


    def _wait_for_games_completion_with_executor(self):
        """Wait for all remaining games to complete using ThreadPoolExecutor"""
        remaining_games = [g for g in self.active_games if g.get_status() != GameStatus.FINISHED]

        if remaining_games:
            print(f"\n⏳ Waiting for {len(remaining_games)} remaining games to complete...")

            with ThreadPoolExecutor(max_workers=len(remaining_games), thread_name_prefix="RemainingGame") as executor:
                future_to_game = {}

                for game in remaining_games:
                    future = executor.submit(self._play_game, game, f"Game {game.get_id()[:8]}")
                    future_to_game[future] = game

                # Process completed games
                for future in as_completed(future_to_game):
                    game = future_to_game[future]
                    try:
                        result = future.result()
                        print(f"✅ Game {game.get_id()[:8]}... completed")
                    except Exception as e:
                        print(f"❌ Game {game.get_id()[:8]}... failed: {e}")

    def _print_summary(self):
        """Print final summary"""
        print("\n🎯 Design Patterns Demonstrated:")
        print("=" * 40)
        print("✅ Singleton Pattern - SnakeAndLadderGame instance")
        print("✅ State Pattern - Game state management")
        print("✅ Observer Pattern - Game notifications")
        print("✅ Factory Pattern - Board and player creation")
        print("✅ Strategy Pattern - Dice rolling strategy")
        print("✅ Concurrency - ThreadPoolExecutor for better resource management")
        print("✅ Thread Safety - Thread-safe game operations")

        print(f"\n📊 Final Statistics:")
        print(f"   • Total games created: {len(self.active_games)}")
        print(f"   • Completed games: {len([g for g in self.active_games if g.get_status() == GameStatus.FINISHED])}")
        print(f"   • Total players across all games: {sum(len(g.get_players()) for g in self.active_games)}")

        # Show winners
        winners = [g.get_winner() for g in self.active_games if g.get_winner()]
        if winners:
            print(f"   • Winners: {[w.get_name() for w in winners]}")


if __name__ == "__main__":
    demo = SnakeAndLadderGameDemo()
    demo.run()
