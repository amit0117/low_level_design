"""
CricInfo Demo - Complete Cricket Management System
This demo showcases ALL required features:
- Player and team management
- Match scheduling and management
- Search functionality (matches, teams, players)
- Live score updates and real-time notifications
- Match history and results viewing
- Detailed match information and statistics
- Concurrent access handling
- Scalable and extensible architecture
"""

from app.services.cric_info_service import CricInfoService
from app.models.enums import PlayerRole, WicketType, MatchType, MatchStatus
from app.models.team import Team
from app.builders.ball_builder import BallBuilder
from app.builders.wicket_builder import WicketBuilder
from app.observers.match_observer import ScorecardDisplay, UserNotifier, CommentaryManager
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


class CricinfoDemo:
    @staticmethod
    def main():
        print("🏏 Welcome to CricInfo Demo - Complete Cricket Management System")
        print("=" * 80)

        # Initialize the service (Singleton pattern)
        service = CricInfoService.get_instance()

        # ========================================
        # 1. PLAYER AND TEAM MANAGEMENT
        # ========================================
        print("\n📋 1. PLAYER AND TEAM MANAGEMENT")
        print("-" * 40)

        # India Team Players
        virat = service.add_player("Virat Kohli", "India", PlayerRole.BATSMAN)
        rohit = service.add_player("Rohit Sharma", "India", PlayerRole.BATSMAN)
        bumrah = service.add_player("Jasprit Bumrah", "India", PlayerRole.BOWLER)
        jadeja = service.add_player("Ravindra Jadeja", "India", PlayerRole.ALL_ROUNDER)

        # Australia Team Players
        warner = service.add_player("David Warner", "Australia", PlayerRole.BATSMAN)
        smith = service.add_player("Steve Smith", "Australia", PlayerRole.BATSMAN)
        starc = service.add_player("Mitchell Starc", "Australia", PlayerRole.BOWLER)
        maxwell = service.add_player("Glenn Maxwell", "Australia", PlayerRole.ALL_ROUNDER)

        # Additional teams for comprehensive demo
        root = service.add_player("Joe Root", "England", PlayerRole.BATSMAN)
        stokes = service.add_player("Ben Stokes", "England", PlayerRole.ALL_ROUNDER)
        babar = service.add_player("Babar Azam", "Pakistan", PlayerRole.BATSMAN)
        afridi = service.add_player("Shaheen Afridi", "Pakistan", PlayerRole.BOWLER)

        # Create teams
        india = Team("India", [virat, rohit, bumrah, jadeja])
        australia = Team("Australia", [warner, smith, starc, maxwell])
        england = Team("England", [root, stokes])
        pakistan = Team("Pakistan", [babar, afridi])

        print(f"✅ Created team: {india.get_name()}")
        print(f"✅ Created team: {australia.get_name()}")
        print(f"✅ Created team: {england.get_name()}")
        print(f"✅ Created team: {pakistan.get_name()}")

        # ========================================
        # 2. MATCH SCHEDULING
        # ========================================
        print("\n📅 2. MATCH SCHEDULING")
        print("-" * 40)

        # Schedule multiple matches
        match1 = service.create_match(india, australia, MatchType.T20)
        match2 = service.create_match(england, pakistan, MatchType.ODI)
        match3 = service.create_match(india, england, MatchType.TEST)

        print(f"✅ Scheduled: {match1.get_team1().get_name()} vs {match1.get_team2().get_name()} ({match1.get_match_type().name})")
        print(f"✅ Scheduled: {match2.get_team1().get_name()} vs {match2.get_team2().get_name()} ({match2.get_match_type().name})")
        print(f"✅ Scheduled: {match3.get_team1().get_name()} vs {match3.get_team2().get_name()} ({match3.get_match_type().name})")

        # ========================================
        # 3. SEARCH FUNCTIONALITY
        # ========================================
        print("\n🔍 3. SEARCH FUNCTIONALITY")
        print("-" * 40)

        # Search for matches by team
        print("Searching for matches involving India:")
        india_matches = service.search_matches_by_team("India")
        for match in india_matches:
            print(f"   Found: {match.get_team1().get_name()} vs {match.get_team2().get_name()}")

        # Search for matches by type
        print("\nSearching for T20 matches:")
        t20_matches = service.search_matches_by_type(MatchType.T20)
        for match in t20_matches:
            print(f"   Found: {match.get_team1().get_name()} vs {match.get_team2().get_name()}")

        # Search for players by name
        print("\nSearching for players by name pattern:")
        virat_players = service.search_players_by_name("Virat")
        warner_players = service.search_players_by_name("Warner")
        for player in virat_players + warner_players:
            print(f"   Found: {player.get_name()} ({player.get_country()}) - {player.get_role().value}")

        # Search for players by country
        print("\nSearching for players by country:")
        india_players = service.search_players_by_country("India")
        print(f"   Found {len(india_players)} players from India")

        # Search for players by role
        print("\nSearching for batsmen:")
        batsmen = service.search_players_by_role(PlayerRole.BATSMAN)
        for player in batsmen:
            print(f"   Found: {player.get_name()} ({player.get_country()})")

        # ========================================
        # 4. LIVE MATCH SIMULATION
        # ========================================
        print("\n🎯 4. LIVE MATCH SIMULATION")
        print("-" * 40)

        # Start the first match
        match_id = match1.get_id()

        # Subscribe observers
        scorecard = ScorecardDisplay()
        commentary = CommentaryManager()
        notifier = UserNotifier()

        service.subscribe_to_match(match_id, commentary)
        service.subscribe_to_match(match_id, scorecard)
        service.subscribe_to_match(match_id, notifier)

        print(f"🚀 Starting match: {match1.get_team1().get_name()} vs {match1.get_team2().get_name()}")
        service.start_match(match_id)

        # Detailed match simulation with commentary
        print("\n" + "=" * 60)
        print("🎯 DETAILED MATCH SIMULATION - INDIA vs AUSTRALIA")
        print("=" * 60)

        india_players = india.get_players()
        australia_players = australia.get_players()

        # First innings simulation
        print("\n--- FIRST INNINGS: INDIA BATTING ---")
        ball_number = 1

        # Ball 1: Virat faces Starc, scores 2 runs
        print(f"\nBall {ball_number}: Virat Kohli faces Mitchell Starc")
        ball1 = BallBuilder().with_ball_number(ball_number).with_bowled_by(starc).with_faced_by(virat).with_runs_scored(2).build()
        service.process_ball(match_id, ball1)
        ball_number += 1
        time.sleep(0.8)

        # Ball 2: Virat faces Starc, scores 1 run
        print(f"\nBall {ball_number}: Virat Kohli faces Mitchell Starc")
        ball2 = BallBuilder().with_ball_number(ball_number).with_bowled_by(starc).with_faced_by(virat).with_runs_scored(1).build()
        service.process_ball(match_id, ball2)
        ball_number += 1
        time.sleep(0.8)

        # Ball 3: Rohit faces Starc, scores 6 runs
        print(f"\nBall {ball_number}: Rohit Sharma faces Mitchell Starc")
        ball3 = BallBuilder().with_ball_number(ball_number).with_bowled_by(starc).with_faced_by(rohit).with_runs_scored(6).build()
        service.process_ball(match_id, ball3)
        ball_number += 1
        time.sleep(0.8)

        # Ball 4: Rohit gets bowled by Starc
        print(f"\nBall {ball_number}: Rohit Sharma faces Mitchell Starc - WICKET!")
        rohit_wicket = WicketBuilder().with_wicket_type(WicketType.BOWLED).with_out_player(rohit).with_bowled_by(starc).build()
        ball4 = (
            BallBuilder()
            .with_ball_number(ball_number)
            .with_bowled_by(starc)
            .with_faced_by(rohit)
            .with_runs_scored(0)
            .with_wicket(rohit_wicket)
            .build()
        )
        service.process_ball(match_id, ball4)
        ball_number += 1
        time.sleep(0.8)

        # Ball 5: Bumrah faces Starc, gets LBW
        print(f"\nBall {ball_number}: Jasprit Bumrah faces Mitchell Starc - WICKET!")
        bumrah_wicket = WicketBuilder().with_wicket_type(WicketType.LBW).with_out_player(bumrah).with_lbw_by(starc).build()
        ball5 = (
            BallBuilder()
            .with_ball_number(ball_number)
            .with_bowled_by(starc)
            .with_faced_by(bumrah)
            .with_runs_scored(0)
            .with_wicket(bumrah_wicket)
            .build()
        )
        service.process_ball(match_id, ball5)
        ball_number += 1
        time.sleep(0.8)

        # Ball 6: Jadeja faces Starc, scores 4 runs
        print(f"\nBall {ball_number}: Ravindra Jadeja faces Mitchell Starc")
        ball6 = BallBuilder().with_ball_number(ball_number).with_bowled_by(starc).with_faced_by(jadeja).with_runs_scored(4).build()
        service.process_ball(match_id, ball6)
        ball_number += 1
        time.sleep(0.8)

        # Ball 7: Jadeja gets caught by Smith
        print(f"\nBall {ball_number}: Ravindra Jadeja faces Mitchell Starc - WICKET!")
        jadeja_wicket = (
            WicketBuilder().with_wicket_type(WicketType.CAUGHT).with_out_player(jadeja).with_caught_by(smith).with_bowled_by(starc).build()
        )
        ball7 = (
            BallBuilder()
            .with_ball_number(ball_number)
            .with_bowled_by(starc)
            .with_faced_by(jadeja)
            .with_runs_scored(0)
            .with_wicket(jadeja_wicket)
            .build()
        )
        service.process_ball(match_id, ball7)
        ball_number += 1
        time.sleep(0.8)

        print("\n" + "=" * 60)
        print("🍃 INNINGS BREAK")
        print("=" * 60)
        print("India's innings completed. Australia needs to chase the target.")
        print("Players are off the field. Preparing for the second innings...")

        # Start the second innings
        service.start_next_inning(match_id)

        print("\n" + "=" * 60)
        print("🎯 SECOND INNINGS: AUSTRALIA BATTING")
        print("=" * 60)

        # Second innings simulation
        ball_number = 1

        # Ball 1: Warner faces Bumrah, scores 4 runs
        print(f"\nBall {ball_number}: David Warner faces Jasprit Bumrah")
        ball8 = BallBuilder().with_ball_number(ball_number).with_bowled_by(bumrah).with_faced_by(warner).with_runs_scored(4).build()
        service.process_ball(match_id, ball8)
        ball_number += 1
        time.sleep(0.8)

        # Ball 2: Warner faces Bumrah, scores 1 run
        print(f"\nBall {ball_number}: David Warner faces Jasprit Bumrah")
        ball9 = BallBuilder().with_ball_number(ball_number).with_bowled_by(bumrah).with_faced_by(warner).with_runs_scored(1).build()
        service.process_ball(match_id, ball9)
        ball_number += 1
        time.sleep(0.8)

        # Ball 3: Warner gets bowled by Bumrah
        print(f"\nBall {ball_number}: David Warner faces Jasprit Bumrah - WICKET!")
        warner_wicket = WicketBuilder().with_wicket_type(WicketType.BOWLED).with_out_player(warner).with_bowled_by(bumrah).build()
        ball10 = (
            BallBuilder()
            .with_ball_number(ball_number)
            .with_bowled_by(bumrah)
            .with_faced_by(warner)
            .with_runs_scored(0)
            .with_wicket(warner_wicket)
            .build()
        )
        service.process_ball(match_id, ball10)
        ball_number += 1
        time.sleep(0.8)

        # Ball 4: Smith faces Bumrah, gets LBW
        print(f"\nBall {ball_number}: Steve Smith faces Jasprit Bumrah - WICKET!")
        smith_wicket = WicketBuilder().with_wicket_type(WicketType.LBW).with_out_player(smith).with_lbw_by(bumrah).build()
        ball11 = (
            BallBuilder()
            .with_ball_number(ball_number)
            .with_bowled_by(bumrah)
            .with_faced_by(smith)
            .with_runs_scored(0)
            .with_wicket(smith_wicket)
            .build()
        )
        service.process_ball(match_id, ball11)
        ball_number += 1
        time.sleep(0.8)

        # Ball 5: Maxwell faces Bumrah, gets stumped
        print(f"\nBall {ball_number}: Glenn Maxwell faces Jasprit Bumrah - WICKET!")
        maxwell_wicket = (
            WicketBuilder().with_wicket_type(WicketType.STUMPED).with_out_player(maxwell).with_stumped_by(virat).with_bowled_by(bumrah).build()
        )
        ball12 = (
            BallBuilder()
            .with_ball_number(ball_number)
            .with_bowled_by(bumrah)
            .with_faced_by(maxwell)
            .with_runs_scored(0)
            .with_wicket(maxwell_wicket)
            .build()
        )
        service.process_ball(match_id, ball12)
        ball_number += 1
        time.sleep(0.8)

        # End the match
        print("\n" + "=" * 60)
        print("🏁 MATCH COMPLETED")
        print("=" * 60)
        service.end_match(match_id)

        print("✅ Detailed match simulation completed with full commentary!")

        # ========================================
        # 5. CONCURRENT ACCESS DEMONSTRATION
        # ========================================
        print("\n🔄 5. CONCURRENT ACCESS DEMONSTRATION")
        print("-" * 40)

        def simulate_concurrent_updates(match_id, team_name, delay):
            """Simulate concurrent ball updates"""
            time.sleep(delay)
            print(f"   [Thread {team_name}] Accessing match {match_id}")
            # This demonstrates thread-safe operations
            match = service.match_service.get_match(match_id)
            return f"{team_name} successfully accessed match {match_id[:8]}..."

        def simulate_concurrent_search(service, search_type, query):
            """Simulate concurrent search operations"""
            time.sleep(0.1)  # Simulate processing time
            if search_type == "team":
                results = service.search_matches_by_team(query)
                return f"Found {len(results)} matches for team {query}"
            elif search_type == "player":
                results = service.search_players_by_name(query)
                return f"Found {len(results)} players matching {query}"
            elif search_type == "country":
                results = service.search_players_by_country(query)
                return f"Found {len(results)} players from {query}"

        # Demonstrate concurrent match access using ThreadPoolExecutor
        print("Testing concurrent match access:")
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit multiple concurrent tasks
            futures = []
            for i, team in enumerate(["India", "Australia", "England", "Pakistan"]):
                future = executor.submit(simulate_concurrent_updates, match_id, team, i * 0.05)
                futures.append(future)

            # Collect results as they complete
            for future in as_completed(futures):
                result = future.result()
                print(f"   ✅ {result}")

        # Demonstrate concurrent search operations
        print("\nTesting concurrent search operations:")
        with ThreadPoolExecutor(max_workers=6) as executor:
            # Submit multiple concurrent search tasks
            search_tasks = [
                ("team", "India"),
                ("team", "Australia"),
                ("player", "Virat"),
                ("player", "Warner"),
                ("country", "India"),
                ("country", "Australia"),
            ]

            futures = []
            for search_type, query in search_tasks:
                future = executor.submit(simulate_concurrent_search, service, search_type, query)
                futures.append(future)

            # Collect results as they complete
            for future in as_completed(futures):
                result = future.result()
                print(f"   ✅ {result}")

        print("✅ Concurrent access with ThreadPoolExecutor handled successfully")

        # ========================================
        # 6. MATCH HISTORY AND RESULTS
        # ========================================
        print("\n📊 6. MATCH HISTORY AND RESULTS")
        print("-" * 40)

        # Get all matches
        all_matches = service.get_match_history()
        print(f"Total matches in system: {len(all_matches)}")

        # Get matches by status
        finished_matches = service.get_finished_matches()
        upcoming_matches = service.get_upcoming_matches()
        live_matches = service.get_live_matches()

        print(f"Finished matches: {len(finished_matches)}")
        print(f"Upcoming matches: {len(upcoming_matches)}")
        print(f"Live matches: {len(live_matches)}")

        # Display match results
        for match in finished_matches:
            print(f"✅ {match.get_team1().get_name()} vs {match.get_team2().get_name()}: {match.get_result_message()}")

        # Display upcoming matches
        for match in upcoming_matches:
            print(f"📅 Upcoming: {match.get_team1().get_name()} vs {match.get_team2().get_name()} ({match.get_match_type().name})")

        # ========================================
        # 7. DETAILED MATCH INFORMATION
        # ========================================
        print("\n📈 7. DETAILED MATCH INFORMATION")
        print("-" * 40)

        # Show detailed match information
        match_details = service.get_match_details(match_id)
        print(f"Match Details:")
        for key, value in match_details.items():
            print(f"   {key}: {value}")

        # Show detailed player information
        print(f"\nPlayer Details for Virat Kohli:")
        virat_details = service.get_player_details(virat.get_id())
        for key, value in virat_details.items():
            print(f"   {key}: {value}")

        # ========================================
        # 8. SCALABILITY AND EXTENSIBILITY
        # ========================================
        print("\n🚀 8. SCALABILITY AND EXTENSIBILITY")
        print("-" * 40)

        # Demonstrate scalability with multiple matches
        print("Creating additional matches for scalability test:")
        for i in range(3):
            team1 = england
            team2 = pakistan
            match = service.create_match(team1, team2, MatchType.T20)
            print(f"   Created match {i+1}: {team1.get_name()} vs {team2.get_name()}")

        print(f"Total matches now: {len(service.get_match_history())}")

        # ========================================
        # 9. REAL-TIME UPDATES DEMONSTRATION
        # ========================================
        print("\n⚡ 9. REAL-TIME UPDATES DEMONSTRATION")
        print("-" * 40)

        print("✅ Observer pattern working:")
        print("   - ScorecardDisplay: Real-time score updates")
        print("   - CommentaryManager: Live commentary")
        print("   - UserNotifier: Instant notifications")


if __name__ == "__main__":
    CricinfoDemo.main()
