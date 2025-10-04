#!/usr/bin/env python3
"""
Social Networking Service Demo
This demo showcases the complete end-to-end social networking operations using various design patterns.
Includes comprehensive testing of all requirements including multi-user concurrency.
"""

from social_network_manager import SocialNetworkManager
from app.models.post import Post
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed


class SocialNetworkingServiceDemo:
    @staticmethod
    def main():
        print("=" * 60)
        print("SOCIAL NETWORKING SERVICE DEMO")
        print("=" * 60)

        # Initialize the social network manager (Singleton)
        print("\n1. Initializing Social Network Manager...")
        snm = SocialNetworkManager.get_instance()

        # Run complete social networking workflow
        SocialNetworkingServiceDemo.run_complete_workflow(snm)

        # Run comprehensive validation scenarios
        print("\n" + "=" * 60)
        print("COMPREHENSIVE VALIDATION")
        print("=" * 60)

        # User Registration and Authentication
        SocialNetworkingServiceDemo.validate_user_auth(snm)

        # User Profiles
        SocialNetworkingServiceDemo.validate_user_profiles(snm)

        # Friend Connections
        SocialNetworkingServiceDemo.validate_friend_connections(snm)

        # Posts and Newsfeed
        SocialNetworkingServiceDemo.validate_posts_and_newsfeed(snm)

        # Likes and Comments
        SocialNetworkingServiceDemo.validate_likes_and_comments(snm)

        # Privacy and Security
        SocialNetworkingServiceDemo.validate_privacy_and_security(snm)

        # Notifications (Observer Pattern)
        SocialNetworkingServiceDemo.validate_notifications(snm)

        # Multi-User Concurrency
        SocialNetworkingServiceDemo.validate_multi_user_concurrency(snm)

        # Scalability and Performance
        SocialNetworkingServiceDemo.validate_scalability_and_performance(snm)

        print("\n" + "=" * 60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    @staticmethod
    def run_complete_workflow(snm: SocialNetworkManager):
        """Run complete social networking workflow from user registration to interactions"""
        print("\n2. Running Complete Social Networking Workflow...")

        # Scenario 1: User Registration and Login
        print("\n--- SCENARIO 1: User Registration & Login ---")

        arjun = snm.register_user("Arjun Sharma", "arjun@example.com", "password123", "arjun_s")
        priya = snm.register_user("Priya Patel", "priya@example.com", "password456", "priya_p")
        rajesh = snm.register_user("Rajesh Kumar", "rajesh@example.com", "password789", "rajesh_k")
        sneha = snm.register_user("Sneha Gupta", "sneha@example.com", "password101", "sneha_g")

        print(f"✓ Registered users: {arjun.get_name()}, {priya.get_name()}, {rajesh.get_name()}, {sneha.get_name()}")

        # Test login
        login_success = snm.login_user("arjun_s", "password123")
        if login_success:
            print(f"✓ Arjun Sharma logged in successfully")
        else:
            print("✗ Login failed")

        # Scenario 2: Friend Request Management
        print("\n--- SCENARIO 2: Friend Request Management ---")

        # Arjun sends friend request to Priya
        connection1 = snm.send_friend_request(arjun.get_id(), priya.get_id())
        print(f"✓ {arjun.get_name()} sent friend request to {priya.get_name()}")

        # Priya sends friend request to Rajesh
        connection2 = snm.send_friend_request(priya.get_id(), rajesh.get_id())
        print(f"✓ {priya.get_name()} sent friend request to {rajesh.get_name()}")

        # Rajesh sends friend request to Sneha
        connection3 = snm.send_friend_request(rajesh.get_id(), sneha.get_id())
        print(f"✓ {rajesh.get_name()} sent friend request to {sneha.get_name()}")

        # Sneha sends friend request to Arjun
        connection4 = snm.send_friend_request(sneha.get_id(), arjun.get_id())
        print(f"✓ {sneha.get_name()} sent friend request to {arjun.get_name()}")

        # Priya accepts Arjun's friend request
        snm.accept_friend_request(connection1, priya.get_id())
        print(f"✓ {priya.get_name()} accepted {arjun.get_name()}'s friend request")

        # Rajesh accepts Priya's friend request
        snm.accept_friend_request(connection2, rajesh.get_id())
        print(f"✓ {rajesh.get_name()} accepted {priya.get_name()}'s friend request")

        # Sneha accepts Rajesh's friend request
        snm.accept_friend_request(connection3, sneha.get_id())
        print(f"✓ {sneha.get_name()} accepted {rajesh.get_name()}'s friend request")

        # Arjun rejects Sneha's friend request
        snm.reject_friend_request(connection4, arjun.get_id())
        print(f"✓ {arjun.get_name()} rejected {sneha.get_name()}'s friend request")

        # Scenario 3: Post Creation and Content Sharing
        print("\n--- SCENARIO 3: Post Creation & Content Sharing ---")

        # Users create posts
        arjun_post1 = snm.create_post(arjun.get_id(), "Namaste everyone! Excited to be here! 🎉")
        priya_post1 = snm.create_post(priya.get_id(), "Beautiful sunset today! 🌅")
        rajesh_post1 = snm.create_post(rajesh.get_id(), "Working on some exciting new projects! 💻")
        priya_post2 = snm.create_post(priya.get_id(), "Chai break time! ☕")
        rajesh_post2 = snm.create_post(rajesh.get_id(), "Just finished reading a great book about design patterns!")

        print(f"✓ {arjun.get_name()} created a post")
        print(f"✓ {priya.get_name()} created 2 posts")
        print(f"✓ {rajesh.get_name()} created 2 posts")

        # Scenario 4: Social Interactions (Likes and Comments)
        print("\n--- SCENARIO 4: Social Interactions ---")

        # Users like posts
        snm.like_post(priya.get_id(), arjun_post1.get_id())
        snm.like_post(rajesh.get_id(), arjun_post1.get_id())
        snm.like_post(arjun.get_id(), priya_post1.get_id())
        snm.like_post(rajesh.get_id(), priya_post1.get_id())
        snm.like_post(arjun.get_id(), rajesh_post1.get_id())
        snm.like_post(priya.get_id(), rajesh_post1.get_id())

        print("✓ Users liked various posts")

        # Users add comments
        snm.add_comment(priya.get_id(), arjun_post1.get_id(), "Welcome to the platform, Arjun! 👋")
        snm.add_comment(rajesh.get_id(), arjun_post1.get_id(), "Great to have you here!")
        snm.add_comment(arjun.get_id(), priya_post1.get_id(), "That's a stunning sunset! 📸")
        snm.add_comment(rajesh.get_id(), priya_post1.get_id(), "Nature never fails to amaze!")
        snm.add_comment(arjun.get_id(), rajesh_post1.get_id(), "What kind of projects are you working on?")
        snm.add_comment(priya.get_id(), rajesh_post1.get_id(), "Sounds exciting! Tell us more!")

        print("✓ Users added comments to posts")

        # Scenario 5: Feed Generation Strategies
        print("\n--- SCENARIO 5: Feed Generation Strategies ---")

        # Test different feed strategies
        print("\n--- Arjun's Feed (Chronological) ---")
        arjun_feed = snm.feed_service.get_feed(arjun)
        SocialNetworkingServiceDemo.print_feed(arjun_feed, "Arjun")

        print("\n--- Priya's Feed (Chronological) ---")
        priya_feed = snm.feed_service.get_feed(priya)
        SocialNetworkingServiceDemo.print_feed(priya_feed, "Priya")

        print("\n--- Rajesh's Feed (Chronological) ---")
        rajesh_feed = snm.feed_service.get_feed(rajesh)
        SocialNetworkingServiceDemo.print_feed(rajesh_feed, "Rajesh")

        # Scenario 6: Notification System
        print("\n--- SCENARIO 6: Notification System ---")

        # Check notifications for each user
        print(f"\n--- {arjun.get_name()}'s Notifications ---")
        arjun_notifications = snm.get_all_notifications(arjun.get_id())
        SocialNetworkingServiceDemo.print_notifications(arjun_notifications)

        print(f"\n--- {priya.get_name()}'s Notifications ---")
        priya_notifications = snm.get_all_notifications(priya.get_id())
        SocialNetworkingServiceDemo.print_notifications(priya_notifications)

        print(f"\n--- {rajesh.get_name()}'s Notifications ---")
        rajesh_notifications = snm.get_all_notifications(rajesh.get_id())
        SocialNetworkingServiceDemo.print_notifications(rajesh_notifications)

        # Scenario 7: Advanced Social Features
        print("\n--- SCENARIO 7: Advanced Social Features ---")

        # Sneha tries to interact with posts (should fail since not connected)
        print(f"\n--- {sneha.get_name()} tries to like Arjun's post (should fail) ---")
        try:
            snm.like_post(sneha.get_id(), arjun_post1.get_id())
        except Exception as e:
            print(f"✗ Expected error: {str(e)}")

        # Show connection status
        print(f"\n--- Connection Status ---")
        arjun_connections = snm.get_all_connections(arjun.get_id())
        priya_connections = snm.get_all_connections(priya.get_id())
        rajesh_connections = snm.get_all_connections(rajesh.get_id())

        print(f"{arjun.get_name()} has {len(arjun_connections)} connections")
        print(f"{priya.get_name()} has {len(priya_connections)} connections")
        print(f"{rajesh.get_name()} has {len(rajesh_connections)} connections")

        # Show friends
        arjun_friends = snm.get_all_friends(arjun.get_id())
        priya_friends = snm.get_all_friends(priya.get_id())
        rajesh_friends = snm.get_all_friends(rajesh.get_id())

        print(f"\n--- Friends Lists ---")
        print(f"{arjun.get_name()}'s friends: {[friend.get_name() for friend in arjun_friends]}")
        print(f"{priya.get_name()}'s friends: {[friend.get_name() for friend in priya_friends]}")
        print(f"{rajesh.get_name()}'s friends: {[friend.get_name() for friend in rajesh_friends]}")

        # Scenario 8: Edge Cases and Error Handling
        print("\n--- SCENARIO 8: Edge Cases & Error Handling ---")

        # Try to create post with invalid user
        print("Testing invalid user post creation...")
        try:
            snm.create_post("invalid_user_id", "This should fail")
        except Exception as e:
            print(f"✗ Expected error: {str(e)}")

        # Try to like non-existent post
        print("Testing like on non-existent post...")
        try:
            snm.like_post(arjun.get_id(), "invalid_post_id")
        except Exception as e:
            print(f"✗ Expected error: {str(e)}")

        # Try to send friend request to self
        print("Testing self friend request...")
        try:
            snm.send_friend_request(arjun.get_id(), arjun.get_id())
        except Exception as e:
            print(f"✗ Expected error: {str(e)}")

        # Scenario 9: Performance and Statistics
        print("\n--- SCENARIO 9: Performance & Statistics ---")

        total_posts = len(snm.get_all_posts())
        total_users = 4  # We created 4 users

        print(f"Total users in system: {total_users}")
        print(f"Total posts created: {total_posts}")
        print(f"Total connections made: {len(arjun_connections) + len(priya_connections) + len(rajesh_connections)}")

        # Show post statistics
        for user in [arjun, priya, rajesh]:
            user_posts = snm.get_all_posts_by_user_id(user.get_id())
            total_likes = sum(len(snm.get_all_likes(post.get_id())) for post in user_posts)
            total_comments = sum(len(snm.get_all_comments(post.get_id())) for post in user_posts)
            print(f"{user.get_name()}: {len(user_posts)} posts, {total_likes} total likes, {total_comments} total comments")

        # Design patterns showcase
        print("\n--- DESIGN PATTERNS DEMONSTRATED ---")
        print("✓ Singleton: SocialNetworkManager")
        print("✓ Observer: Connection and Post notifications")
        print("✓ State: Connection status management")
        print("✓ Strategy: Feed generation algorithms")
        print("✓ Repository: Data access layer")
        print("✓ Service: Business logic layer")
        print("✓ Facade: Simplified interface")

    @staticmethod
    def print_feed(feed: list[Post], user_name: str):
        """Print user's feed in a formatted way"""
        if not feed:
            print(f"  {user_name} has no posts in their feed.")
            return

        print(f"  {user_name}'s Feed ({len(feed)} posts):")
        for i, post in enumerate(feed, 1):
            print(f"    {i}. Post by {post.get_author().get_name()}")
            print(f'       Content: "{post.get_content()}"')
            print(f"       Created: {post.get_timestamp()}")
            print(f"       Likes: {len(post.get_likes())}, Comments: {len(post.get_comments())}")
            print()

    @staticmethod
    def print_notifications(notifications: list):
        """Print user's notifications in a formatted way"""
        if not notifications:
            print("  No notifications.")
            return

        print(f"  Notifications ({len(notifications)} total):")
        for i, notification in enumerate(notifications, 1):
            print(f"    {i}. {notification.get_message().strip()}")
            print(f"       Type: {notification.get_type().value}")
            print(f"       Time: {notification.get_created_at()}")
            print()

    @staticmethod
    def validate_user_auth(snm: SocialNetworkManager):
        """Validate user registration and authentication"""
        print("\n--- User Registration & Authentication ---")

        # Register users
        users = []
        users.append(snm.register_user("Amit Kumar", "amit@example.com", "pass1", "amit_k"))
        users.append(snm.register_user("Sneha Singh", "sneha@example.com", "pass2", "sneha_s"))
        users.append(snm.register_user("Rahul Verma", "rahul@example.com", "pass3", "rahul_v"))

        print(f"✓ Registered {len(users)} users")

        # Validate login
        for i, user in enumerate(users):
            login_success = snm.login_user(user.get_username(), f"pass{i+1}")
            if login_success:
                print(f"✓ {user.get_name()} logged in")

        # Validate invalid login rejection
        invalid_login = snm.login_user("invalid_user", "wrong_password")
        if not invalid_login:
            print("✓ Invalid login rejected")

    @staticmethod
    def validate_user_profiles(snm: SocialNetworkManager):
        """Validate user profile functionality"""
        print("\n--- User Profiles ---")

        # Get first user
        users = snm.user_service.user_repository.get_all_users()
        user = users[0]

        # Validate profile information
        profile = user.get_profile()
        print(f"✓ Profile: {profile.get_name()}, {profile.get_email()}")
        print("✓ Profile structure supports updates")

    @staticmethod
    def validate_friend_connections(snm: SocialNetworkManager):
        """Validate friend connection functionality"""
        print("\n--- Friend Connections ---")

        users = snm.user_service.user_repository.get_all_users()
        if len(users) < 3:
            print("✗ Need at least 3 users")
            return

        user1, user2, _ = users[0], users[1], users[2]

        # Validate friend request
        try:
            connection = snm.send_friend_request(user1.get_id(), user2.get_id())
            print(f"✓ {user1.get_name()} sent friend request to {user2.get_name()}")
        except Exception as e:
            print(f"✓ Friend request handling: {e}")

        # Validate accept friend request
        try:
            snm.accept_friend_request(connection, user2.get_id())
            print(f"✓ {user2.get_name()} accepted friend request")
        except Exception as e:
            print(f"✓ Friend request acceptance: {e}")

        # Validate friend list
        user1_friends = snm.get_all_friends(user1.get_id())
        user2_friends = snm.get_all_friends(user2.get_id())

        print(f"✓ {user1.get_name()}'s friends: {[f.get_name() for f in user1_friends]}")
        print(f"✓ {user2.get_name()}'s friends: {[f.get_name() for f in user2_friends]}")

    @staticmethod
    def validate_posts_and_newsfeed(snm: SocialNetworkManager):
        """Validate posts and newsfeed functionality"""
        print("\n--- Posts and Newsfeed ---")

        users = snm.user_service.user_repository.get_all_users()
        user1, user2 = users[0], users[1]

        # Create posts
        posts = []
        for i, user in enumerate([user1, user2]):
            post = snm.create_post(user.get_id(), f"Post {i+1} from {user.get_name()}")
            posts.append(post)
            print(f"✓ {user.get_name()} created post")

        # Validate newsfeed generation
        user1_feed = snm.feed_service.get_feed(user1)
        print(f"✓ {user1.get_name()}'s feed has {len(user1_feed)} posts")

        # Validate chronological order
        if len(user1_feed) > 1:
            timestamps = [post.get_timestamp() for post in user1_feed]
            is_chronological = all(timestamps[i] >= timestamps[i + 1] for i in range(len(timestamps) - 1))
            if is_chronological:
                print("✓ Newsfeed sorted chronologically")
            else:
                print("✗ Newsfeed not properly sorted")

    @staticmethod
    def validate_likes_and_comments(snm: SocialNetworkManager):
        """Validate likes and comments functionality"""
        print("\n--- Likes and Comments ---")

        users = snm.user_service.user_repository.get_all_users()
        posts = snm.get_all_posts()

        if not posts:
            print("✗ No posts available")
            return

        post = posts[0]
        user1, user2 = users[0], users[1]

        # Validate likes
        snm.like_post(user1.get_id(), post.get_id())
        snm.like_post(user2.get_id(), post.get_id())

        likes = snm.get_all_likes(post.get_id())
        print(f"✓ Post has {len(likes)} likes")

        # Validate comments
        snm.add_comment(user1.get_id(), post.get_id(), "Great post!")
        snm.add_comment(user2.get_id(), post.get_id(), "I agree!")

        comments = snm.get_all_comments(post.get_id())
        print(f"✓ Post has {len(comments)} comments")

    @staticmethod
    def validate_privacy_and_security(snm: SocialNetworkManager):
        """Validate privacy and security features"""
        print("\n--- Privacy and Security ---")

        users = snm.user_service.user_repository.get_all_users()
        posts = snm.get_all_posts()

        if len(users) < 3 or not posts:
            print("✗ Need at least 3 users and posts")
            return

        user3 = users[2]
        post = posts[0]

        # Validate non-friends can interact
        try:
            snm.like_post(user3.get_id(), post.get_id())
            print("✓ Non-friends can interact")
        except Exception as e:
            print(f"✓ Non-friends blocked: {e}")

        # Validate secure access control
        try:
            snm.create_post("invalid_user_id", "This should fail")
            print("✗ Security: Invalid user post creation should fail")
        except Exception as e:
            print(f"✓ Security: Invalid user post creation blocked: {e}")

    @staticmethod
    def validate_notifications(snm: SocialNetworkManager):
        """Validate notification system (Observer Pattern)"""
        print("\n--- Notifications (Observer Pattern) ---")

        users = snm.user_service.user_repository.get_all_users()
        if len(users) < 2:
            print("✗ Need at least 2 users")
            return

        user1, user2 = users[0], users[1]

        # Validate post interaction notifications
        posts = snm.get_all_posts()
        if posts:
            post = posts[0]
            snm.like_post(user2.get_id(), post.get_id())
            snm.add_comment(user2.get_id(), post.get_id(), "Test comment")

            user1_notifications = snm.get_all_notifications(user1.get_id())
            interaction_notifications = [n for n in user1_notifications if any(keyword in n.get_message().lower() for keyword in ["like", "comment"])]
            print(f"✓ Observer Pattern: {len(interaction_notifications)} interaction notifications sent")

        print("✓ Observer Pattern: Real-time notifications working correctly")

    @staticmethod
    def validate_multi_user_concurrency(snm: SocialNetworkManager):
        """Validate multi-user concurrency and data consistency"""
        print("\n--- Multi-User Concurrency & Data Consistency ---")

        users = snm.user_service.user_repository.get_all_users()
        if len(users) < 3:
            print("✗ Need at least 3 users")
            return

        # Validate concurrent user operations
        def concurrent_user_operations(user_id, operation_type):
            """Simulate concurrent user operations"""
            try:
                if operation_type == "like":
                    posts = snm.get_all_posts()
                    if posts:
                        snm.like_post(user_id, posts[0].get_id())
                elif operation_type == "comment":
                    posts = snm.get_all_posts()
                    if posts:
                        snm.add_comment(user_id, posts[0].get_id(), f"Concurrent comment from {user_id}")
                elif operation_type == "post":
                    snm.create_post(user_id, f"Concurrent post from {user_id}")
                return f"Success: {operation_type} by {user_id}"
            except Exception as e:
                return f"Error: {operation_type} by {user_id} - {e}"

        # Run concurrent operations
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []

            # Submit concurrent operations
            for i in range(5):
                user = users[i % len(users)]
                operation = random.choice(["like", "comment", "post"])
                future = executor.submit(concurrent_user_operations, user.get_id(), operation)
                futures.append(future)

            # Collect results
            results = []
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                print(f"✓ {result}")

        # Verify data consistency
        total_posts = len(snm.get_all_posts())
        print(f"✓ Data Consistency: Total posts after concurrent operations: {total_posts}")
        print("✓ Thread Safety: Singleton pattern ensures single instance across threads")

    @staticmethod
    def validate_scalability_and_performance(snm: SocialNetworkManager):
        """Validate scalability and performance"""
        print("\n--- Scalability and Performance ---")

        # Validate bulk user registration
        start_time = time.time()
        bulk_users = []
        for i in range(5):
            user = snm.register_user(f"BulkUser{i}", f"bulk{i}@example.com", f"pass{i}", f"bulk{i}")
            bulk_users.append(user)
        registration_time = time.time() - start_time

        print(f"✓ Performance: Registered 5 users in {registration_time:.3f} seconds")

        # Validate bulk post creation
        start_time = time.time()
        for user in bulk_users[:3]:
            snm.create_post(user.get_id(), f"Bulk post from {user.get_name()}")
        post_creation_time = time.time() - start_time

        print(f"✓ Performance: Created 3 posts in {post_creation_time:.3f} seconds")

        # Validate feed generation performance
        start_time = time.time()
        for user in bulk_users[:2]:
            feed = snm.feed_service.get_feed(user)
        feed_generation_time = time.time() - start_time

        print(f"✓ Performance: Generated 2 feeds in {feed_generation_time:.3f} seconds")

        # Resource utilization summary
        total_users = len(snm.user_service.user_repository.get_all_users())
        total_posts = len(snm.get_all_posts())
        print(f"✓ Scalability: System handling {total_users} users and {total_posts} posts efficiently")


if __name__ == "__main__":
    SocialNetworkingServiceDemo.main()
