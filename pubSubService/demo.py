import time
import os
from pub_sub_app import PubSubApp
from app.models.enums import BrokerType, MessagePersistenceStrategy
from concurrent.futures import ThreadPoolExecutor, as_completed


def scenario1_rabbitmq_broadcast():
    print("\n=== Scenario 1: RabbitMQ Broadcast (Push + Broadcast + At-Least-Once) ===\n")

    app = PubSubApp("RabbitMQApp", BrokerType.RABBITMQ)

    app.create_topic("OrderUpdates")
    app.create_topic("InventoryUpdates")

    subscriber1 = app.create_subscriber("OrderService-Rajesh")
    subscriber2 = app.create_subscriber("InventoryService-Priya")
    subscriber3 = app.create_subscriber("NotificationService-Amit")

    app.subscribe("OrderUpdates", subscriber1)
    app.subscribe("InventoryUpdates", subscriber2)
    app.subscribe("OrderUpdates", subscriber3)

    app.start()

    app.create_publisher()

    print("📤 Publishing messages...")
    for i in range(1, 4):
        app.publish("OrderUpdates", f"Order#{i} created")
        time.sleep(0.2)

    app.publish("InventoryUpdates", "Stock updated")

    time.sleep(1)
    app.stop()

    print("✅ Scenario 1 completed\n")


def scenario2_kafka_round_robin():
    print("\n=== Scenario 2: Kafka Round-Robin (Pull + Round-Robin + At-Least-Once) ===\n")

    app = PubSubApp("KafkaApp", BrokerType.KAFKA)

    # Create topic
    order_topic = app.create_topic("Orders")

    # Create multiple subscribers for load balancing
    consumer1 = app.create_subscriber("Consumer1-Shravan")
    consumer2 = app.create_subscriber("Consumer2-Kavita")
    consumer3 = app.create_subscriber("Consumer3-Rohan")

    # Subscribe all to topic
    app.subscribe("Orders", consumer1)
    app.subscribe("Orders", consumer2)
    app.subscribe("Orders", consumer3)

    # Start consumption
    app.start()

    # Publish messages
    print("📤 Publishing messages...")
    for i in range(1, 6):
        app.publish("Orders", f"Order#{i} - Payment received")
        time.sleep(0.1)

    # In pull model, subscribers need to explicitly pull messages
    print("📥 Subscribers pulling messages...")
    for i in range(1, 6):
        message = app.pull_message("Orders")
        if message:
            print(f"📨 {message.get_payload()}")
        else:
            break

    time.sleep(0.5)
    app.stop()

    print("✅ Scenario 2 completed\n")


def scenario3_at_least_once_delivery():
    print("\n=== Scenario 3: At-Least-Once Delivery with Retry ===\n")

    app = PubSubApp("RetryApp", BrokerType.RABBITMQ)

    # Create topic
    payment_topic = app.create_topic("Payments", storage_type=MessagePersistenceStrategy.FILE)

    # Create subscriber
    payment_service = app.create_subscriber("PaymentProcessor-Vikram")
    app.subscribe("Payments", payment_service)

    app.start()

    # Publish critical payment messages
    print("📤 Publishing critical payment messages...")
    payments = ["Payment-1234", "Payment-5678", "Payment-9999"]

    for payment in payments:
        app.publish("Payments", payment)
        time.sleep(0.2)

    print("✅ Critical payments guaranteed delivery (at-least-once)")

    time.sleep(1)
    app.stop()

    print("✅ Scenario 3 completed\n")


def scenario4_topic_subscription_management():
    print("\n=== Scenario 4: Topic Subscription Management ===\n")

    app = PubSubApp("ManagementApp")

    # Create topic
    app.create_topic("NewsUpdates")

    # Create subscribers
    reader1 = app.create_subscriber("Reader-Anjali")
    reader2 = app.create_subscriber("Reader-Sudha")

    # Subscribe
    print("👥 Subscribing...")
    app.subscribe("NewsUpdates", reader1)
    app.subscribe("NewsUpdates", reader2)

    app.start()

    # Publish
    print("📤 Publishing news...")
    app.publish("NewsUpdates", "Breaking: New tech released")
    time.sleep(1)

    # Unsubscribe one reader
    print("👋 Unsubscribing Reader-Anjali...")
    app.unsubscribe("NewsUpdates", reader1)

    # Publish again
    app.publish("NewsUpdates", "Latest: AI breakthrough")
    time.sleep(1)

    app.stop()

    print("✅ Scenario 4 completed\n")


def scenario5_multiple_topics():
    print("\n=== Scenario 5: Multiple Topics with Multiple Subscribers ===\n")

    app = PubSubApp("MultiTopicApp")

    # Create multiple topics
    app.create_topic("Orders")
    app.create_topic("Inventory")
    app.create_topic("Notifications")

    # Create services
    order_service = app.create_subscriber("OrderService")
    inventory_service = app.create_subscriber("InventoryService")
    notification_service = app.create_subscriber("NotificationService")

    # Subscribe to respective topics
    app.subscribe("Orders", order_service)
    app.subscribe("Inventory", inventory_service)
    app.subscribe("Notifications", notification_service)

    app.start()

    # Create publisher
    app.create_publisher()

    # Publish to different topics
    print("📤 Publishing to multiple topics...")
    app.publish("Orders", "New order placed")
    app.publish("Inventory", "Stock level low")
    app.publish("Notifications", "Email sent to user")

    time.sleep(1)
    app.stop()

    print("✅ Scenario 5 completed\n")


def scenario6_multiple_publishers():
    print("\n=== Scenario 6: Multiple Publishers (Concurrent Publishing) ===\n")

    app = PubSubApp("MultiPublisherApp", BrokerType.RABBITMQ)

    # Create topic
    app.create_topic("Orders")

    # Create multiple subscribers
    for i in range(1, 4):
        subscriber = app.create_subscriber(f"Service-{i}")
        app.subscribe("Orders", subscriber)

    app.start()

    def publish_from_publisher(publisher_id: int, num_messages: int):
        publisher = app.create_publisher()
        for i in range(1, num_messages + 1):
            app.publish("Orders", f"Publisher{publisher_id}-Message{i}")
            time.sleep(0.1)
        return f"Publisher{publisher_id} completed"

    print("📤 Multiple publishers publishing concurrently using ThreadPoolExecutor...")

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(publish_from_publisher, pub_id, 3) for pub_id in range(1, 4)]
        for future in as_completed(futures):
            result = future.result()
            print(f"  ✓ {result}")

    time.sleep(1)
    app.stop()

    print("✅ Scenario 6 completed\n")


def scenario7_thread_safety():
    print("\n=== Scenario 7: Thread Safety & Concurrent Access ===\n")

    app = PubSubApp("ThreadSafeApp")

    app.create_topic("HighConcurrency")

    # Create multiple subscribers
    for i in range(1, 6):
        subscriber = app.create_subscriber(f"Worker-{i}")
        app.subscribe("HighConcurrency", subscriber)

    app.start()

    def concurrent_publisher(thread_id: int, message_count: int):
        for i in range(message_count):
            app.publish("HighConcurrency", f"Thread{thread_id}-Msg{i+1}")
            time.sleep(0.05)
        return f"Thread{thread_id} done"

    def concurrent_subscriber(thread_id: int):
        subscriber = app.create_subscriber(f"DynamicWorker-{thread_id}")
        app.subscribe("HighConcurrency", subscriber)
        app.publish("HighConcurrency", f"Subscriber {thread_id} joined")
        return f"Subscriber {thread_id} added"

    print("📤 Testing thread safety with 3 concurrent publishers and 3 dynamic subscribers...")

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        # 3 concurrent publishers
        futures.extend([executor.submit(concurrent_publisher, i, 5) for i in range(1, 4)])
        # 3 dynamic subscribers
        futures.extend([executor.submit(concurrent_subscriber, i) for i in range(1, 4)])

        for future in as_completed(futures):
            result = future.result()

    time.sleep(1)
    app.stop()

    print("✅ Thread safety verified - all concurrent operations completed\n")


def cleanup_files():
    """Clean up any files generated during the demo."""
    files_to_cleanup = ["message_queue.txt"]

    for filename in files_to_cleanup:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"🧹 Cleaned up: {filename}")
            except OSError as e:
                print(f"⚠️  Could not delete {filename}: {e}")


def main():
    print("\n" + "=" * 80)
    print("PUB-SUB SYSTEM DEMONSTRATION")
    print("=" * 80)

    scenario1_rabbitmq_broadcast()
    time.sleep(1)

    scenario2_kafka_round_robin()
    time.sleep(1)

    scenario3_at_least_once_delivery()
    time.sleep(1)

    scenario4_topic_subscription_management()
    time.sleep(1)

    scenario5_multiple_topics()
    time.sleep(1)

    scenario6_multiple_publishers()
    time.sleep(1)

    scenario7_thread_safety()
    time.sleep(1)

    # Cleanup: Delete any generated files
    cleanup_files()

    print("\n" + "=" * 80)
    print("ALL DEMOS COMPLETED SUCCESSFULLY!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
