"""
Factory Pattern for creating Pub-Sub entities
Provides convenient factory methods for common Pub-Sub configurations
"""

from app.models.broker import Broker
from app.models.pubisher import Publisher
from app.models.subscriber import MessageSubscriber
from app.models.topic import Topic
from app.models.message import Message
from app.models.message_queue import MessageQueue
from app.strategies.message_persistence_strategy import inMemoryMessageQueueStrategy, fileMessageQueueStrategy
from app.strategies.message_routing_strategy import BroadCastMessageRoutingStrategy, RoundRobinMessageRoutingStrategy
from app.strategies.message_delivery_strategy import AtMostOnce, AtLeastOnce
from app.strategies.message_retry_strategy import FixedIntervalRetry, ExponentialBackoffRetry, JitterRetry
from app.strategies.message_consumption_strategy import PushConsumptionStrategy, PullConsumptionStrategy


class PubSubFactory:
    """
    Factory for creating Pub-Sub entities with common configurations.
    Follows the Factory Pattern to encapsulate object creation logic.
    """

    @staticmethod
    def create_broker(name: str = "Broker", consumption_model: str = "push", delivery_guarantee: str = "at-most-once") -> Broker:
        """
        Create a broker with common configurations.

        Args:
            name: Name of the broker
            consumption_model: "push" or "pull"
            delivery_guarantee: "at-most-once" or "at-least-once"

        Returns:
            Configured Broker instance
        """
        # Select consumption strategy
        if consumption_model.lower() == "pull":
            consumption_strategy = PullConsumptionStrategy(broker=None)
        else:  # Default to push
            consumption_strategy = PushConsumptionStrategy(broker=None)

        # Create broker
        broker = Broker(name=name, consumption_strategy=consumption_strategy)

        # Configure delivery strategy
        if delivery_guarantee.lower() == "at-least-once":
            broker.delivery_strategy = AtLeastOnce(retry_strategy=ExponentialBackoffRetry(retries=5, base_delay=1))
        else:  # at-most-once
            broker.delivery_strategy = AtMostOnce(retry_strategy=FixedIntervalRetry(retries=2, interval=1))

        return broker

    @staticmethod
    def create_topic_with_queue(topic_name: str, storage_type: str = "in-memory") -> tuple[Topic, MessageQueue]:
        """
        Create a topic with its associated queue.

        Args:
            topic_name: Name of the topic
            storage_type: "in-memory" or "file"

        Returns:
            Tuple of (Topic, MessageQueue)
        """
        topic = Topic(topic_name)

        # Select queue storage strategy
        if storage_type.lower() == "file":
            queue_strategy = fileMessageQueueStrategy()
        else:  # Default to in-memory
            queue_strategy = inMemoryMessageQueueStrategy()

        queue = MessageQueue(strategy=queue_strategy)

        return topic, queue

    @staticmethod
    def create_publisher(broker: Broker) -> Publisher:
        """Create a publisher for the given broker."""
        return Publisher(broker)

    @staticmethod
    def create_subscriber(name: str) -> MessageSubscriber:
        return MessageSubscriber(name)

    @staticmethod
    def create_message(topic: Topic, payload: str, message_id: str = None) -> Message:
        return Message(topic=topic, payload=payload, id=message_id)

    @staticmethod
    def setup_complete_pub_sub_system(
        broker_name: str = "MainBroker", consumption_model: str = "push", delivery_guarantee: str = "at-most-once"
    ) -> Broker:
        """
        Create a complete pub-sub system with all components configured.

        Args:
            broker_name: Name of the broker
            consumption_model: "push" or "pull"
            delivery_guarantee: "at-most-once" or "at-least-once"

        Returns:
            Fully configured Broker instance

        Example:
            broker = PubSubFactory.setup_complete_pub_sub_system()
            topic, queue = PubSubFactory.create_topic_with_queue("Orders")
            broker.add_topic(topic, queue)

            subscriber = PubSubFactory.create_subscriber("OrderService")
            topic.subscribe(subscriber)

            publisher = PubSubFactory.create_publisher(broker)
            message = PubSubFactory.create_message(topic, "Order#123 created")
            publisher.publish(message)

            broker.start_consumption()
        """
        return PubSubFactory.create_broker(broker_name, consumption_model, delivery_guarantee)


class BrokerConfigFactory:
    """Factory for creating brokers with specific configurations."""

    @staticmethod
    def create_rabbitmq_like_broker(name: str = "RabbitMQBroker") -> Broker:
        """Create a broker configured like RabbitMQ (Push + At-Least-Once + Broadcast)."""
        broker = Broker(name=name, consumption_strategy=PushConsumptionStrategy(broker=None))
        broker.routing_strategy = BroadCastMessageRoutingStrategy()
        broker.delivery_strategy = AtLeastOnce(retry_strategy=ExponentialBackoffRetry(retries=5, base_delay=1))
        return broker

    @staticmethod
    def create_kafka_like_broker(name: str = "KafkaBroker") -> Broker:
        """Create a broker configured like Kafka (Pull + At-Least-Once + Round-Robin)."""
        broker = Broker(name=name, consumption_strategy=PullConsumptionStrategy(broker=None))
        broker.routing_strategy = RoundRobinMessageRoutingStrategy()
        broker.delivery_strategy = AtLeastOnce(retry_strategy=ExponentialBackoffRetry(retries=5, base_delay=1))
        return broker

    @staticmethod
    def create_sqs_like_broker(name: str = "SQSBroker") -> Broker:
        """Create a broker configured like AWS SQS (Pull + At-Least-Once + Round-Robin)."""
        broker = Broker(name=name, consumption_strategy=PullConsumptionStrategy(broker=None))
        broker.routing_strategy = RoundRobinMessageRoutingStrategy()
        broker.delivery_strategy = AtLeastOnce(retry_strategy=JitterRetry(retries=3, base_delay=2, max_delay=10))
        return broker


class StrategyFactory:
    """Factory for creating specific strategy configurations."""

    @staticmethod
    def create_fast_retry_strategy():
        """Fast retry with fixed interval."""
        return FixedIntervalRetry(retries=3, interval=1)

    @staticmethod
    def create_safe_retry_strategy():
        """Safe retry with exponential backoff."""
        return ExponentialBackoffRetry(retries=5, base_delay=1, max_delay=32)

    @staticmethod
    def create_jitter_retry_strategy():
        """Jitter retry to avoid thundering herd."""
        return JitterRetry(retries=5, base_delay=1, max_delay=10)
