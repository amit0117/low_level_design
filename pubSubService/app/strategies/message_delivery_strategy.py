from abc import ABC, abstractmethod
import time
from app.models.subscriber import MessageSubscriber
from app.models.message import Message
from app.strategies.message_retry_strategy import MessageRetryStrategy


class MessageDeliveryStrategy(ABC):
    def __init__(self, retry_strategy: MessageRetryStrategy):
        self.retry_strategy = retry_strategy

    @abstractmethod
    def deliver(self, subscriber: MessageSubscriber, message: Message) -> bool:
        raise NotImplementedError("Subclasses must implement this method")


class AtMostOnce(MessageDeliveryStrategy):
    def deliver(self, subscriber: MessageSubscriber, message: Message) -> bool:
        try:
            subscriber.receive(message)
        except Exception:
            return self.retry_strategy.retry(subscriber.receive, message)
        return True


class AtLeastOnce(MessageDeliveryStrategy):
    def deliver(self, subscriber: MessageSubscriber, message: Message) -> bool:
        """
        At Least Once Delivery: Guarantees message is delivered at least once.
        Uses infinite retries to ensure delivery succeeds (true at-least-once guarantee).
        The same message may be delivered multiple times if failures occur.
        """

        def _deliver_message(msg: Message) -> None:
            subscriber.receive(msg)
            if not subscriber.acknowledge(msg):
                raise Exception(f"Subscriber {subscriber.get_name()} failed to acknowledge message {msg.get_id()}")

        # Try once directly
        try:
            _deliver_message(message)
            return True
        except Exception:
            pass

        # Use retry strategy for subsequent attempts with backoff
        # Keep retrying until success (true at-least-once guarantee)
        attempt = 0
        while True:
            attempt += 1
            # Use retry strategy which handles backoff and retries
            success = self.retry_strategy.retry(_deliver_message, message)
            if success:
                return True
            # If retry strategy exhausted, wait and try again (infinite retries)
            time.sleep(1)
