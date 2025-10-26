from app.models.message import Message
from app.models.message_queue import MessageQueue
from app.strategies.message_routing_strategy import MessageRoutingStrategy, RoundRobinMessageRoutingStrategy
from app.models.topic import Topic
from uuid import uuid4
from app.strategies.message_delivery_strategy import MessageDeliveryStrategy, AtMostOnce
from app.strategies.message_retry_strategy import FixedIntervalRetry
from app.strategies.message_consumption_strategy import MessageConsumptionStrategy, PushConsumptionStrategy, PullConsumptionStrategy


class Broker:
    def __init__(self, name: str = "Broker", consumption_strategy: MessageConsumptionStrategy = None) -> None:
        self.broker_id = str(uuid4())
        self.name = name
        self.queues: dict[Topic, MessageQueue] = {}
        self.routing_strategy: MessageRoutingStrategy = RoundRobinMessageRoutingStrategy()
        self.delivery_strategy: MessageDeliveryStrategy = AtMostOnce(retry_strategy=FixedIntervalRetry(retries=3, interval=2))
        # Single consumption strategy for the entire broker
        if consumption_strategy is None:
            consumption_strategy = PushConsumptionStrategy(broker=None)
        self.consumption_strategy: MessageConsumptionStrategy = consumption_strategy
        # Set broker reference after initialization
        self.consumption_strategy.broker = self

    def add_topic(self, topic: Topic, queue: MessageQueue) -> None:
        """Add a topic with its queue."""
        self.queues[topic] = queue

    def publish(self, message: Message) -> bool:
        """
        Publish message to topic's queue.
        Message will be consumed based on the broker's consumption strategy.
        """
        try:
            topic = message.get_topic()

            # First try direct lookup
            if topic in self.queues:
                self.queues[topic].add_message_to_queue(message)
                # Message published to topic {topic.get_name()}
                return True

            # If direct lookup fails, try to find by name
            for broker_topic in self.queues.keys():
                if broker_topic.get_name() == topic.get_name():
                    self.queues[broker_topic].add_message_to_queue(message)
                    # Message published to topic {topic.get_name()}
                    return True

            # Debug: Show what topics are actually in the broker
            print(f"❌ Topic '{topic.get_name()}' not found. Available topics in broker: {[t.get_name() for t in self.queues.keys()]}")
            return False
        except Exception as e:
            print(f"❌ Error publishing message: {e}")
            return False

    def start_consumption(self) -> None:
        """Start message consumption using the broker's consumption strategy."""
        self.consumption_strategy.start()

    def stop_consumption(self) -> None:
        """Stop message consumption."""
        self.consumption_strategy.stop()

    def route_and_deliver(self, message: Message) -> None:
        """
        Route message to subscribers using routing strategy,
        then deliver using delivery strategy (handles retry, acknowledgement).
        """
        target_subscribers = self.routing_strategy.route(message)

        if not target_subscribers:
            return

        # Deliver to each target subscriber using delivery strategy
        for subscriber in target_subscribers:
            success = self.delivery_strategy.deliver(subscriber, message)
            # Delivery failed silently - retry strategy handles failures

    def pull_message(self, topic: Topic) -> Message:
        """
        Pull consumption model: Subscribers explicitly pull messages.
        Returns the next message from the topic's queue.
        """
        if topic not in self.queues:
            raise ValueError(f"Topic {topic.get_name()} not found")
        return self.queues[topic].get_message_from_queue()
