from abc import ABC, abstractmethod
from app.models.topic import Topic
from app.models.message_queue import MessageQueue
import threading
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.broker import Broker


class MessageConsumptionStrategy(ABC):
    """Base strategy for message consumption models (Push vs Pull)."""

    @abstractmethod
    def start(self, broker) -> None:
        """Start consumption for all topics in the broker."""
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def stop(self) -> None:
        """Stop consumption."""
        raise NotImplementedError("Subclasses must implement this method")


class PushConsumptionStrategy(MessageConsumptionStrategy):
    """
    Push Model: Broker actively pushes messages to subscribers.
    Consumers are notified as soon as messages arrive.
    Like RabbitMQ's basic.consume or Redis Pub/Sub.
    """

    def __init__(self, broker: "Broker"):
        self.broker = broker
        self.running = False
        self.threads: list[threading.Thread] = []

    def start(self) -> None:
        """Start push consumption for all topics in the broker."""
        if self.running:
            return

        self.running = True

        # Start a consumer thread for each topic
        for topic, queue in self.broker.queues.items():
            thread = threading.Thread(target=self._push_loop, args=(topic, queue), daemon=True, name=f"PushConsumer-{topic.get_name()}")
            self.threads.append(thread)
            thread.start()

        print(f"🚀 Push consumption started for {len(self.broker.queues)} topic(s)")

    def stop(self) -> None:
        """Stop push consumption."""
        if not self.running:
            return

        self.running = False

        # Stop all queue strategies to wake up blocked threads
        for topic, queue in self.broker.queues.items():
            if hasattr(queue.message_queue_strategy, "stop"):
                queue.message_queue_strategy.stop()

        # Wait for all threads to finish (with timeout)
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=1.0)  # Wait up to 1 second for each thread

        self.threads.clear()
        print("✅ Push consumption stopped")

    def _push_loop(self, topic: Topic, queue: MessageQueue) -> None:
        """Continuously consume messages and notify subscribers immediately."""
        # Consumer loop running for topic {topic.get_name()}

        while self.running:
            try:
                # Blocking dequeue - waits for new messages (uses condition variable) when consumer is pull based like Kafka and persistence strategy is inMemoryMessageQueueStrategy
                if not self.running:  # Check before blocking
                    break

                message = queue.get_message_from_queue()

                if not self.running:  # Check after being woken
                    break

                # Route and deliver immediately
                self.broker.route_and_deliver(message)

            except Exception as e:
                # If interrupted or queue operations fail, check if we should continue
                if not self.running:
                    break
                # Continue polling
                time.sleep(0.1)
                continue

        # Consumer loop stopped for topic {topic.get_name()}


class PullConsumptionStrategy(MessageConsumptionStrategy):
    """
    Pull Model: Subscribers explicitly request messages when they're ready.
    Like Kafka's consumer API or AWS SQS receive messages.
    The queue's condition variable handles blocking until messages are available.
    """

    def __init__(self, broker: "Broker"):
        self.broker = broker

    def start(self) -> None:
        """Start pull consumption - subscribers will pull messages on demand."""
        print("🔄 Pull consumption configured")

    def stop(self) -> None:
        """Stop pull consumption."""
        print("✅ Pull consumption stopped")
