from abc import ABC, abstractmethod
from app.models.message import Message
from app.models.subscriber import MessageSubscriber
from typing import List


class MessageRoutingStrategy(ABC):
    @abstractmethod
    def route(self, message: Message) -> List[MessageSubscriber]:
        """
        Returns list of subscribers that should receive this message.
        Broker will use delivery strategy to actually deliver with retry/ack.
        """
        raise NotImplementedError("Subclasses must implement this method")


class BroadCastMessageRoutingStrategy(MessageRoutingStrategy):
    def route(self, message: Message) -> List[MessageSubscriber]:
        """Broadcast: All subscribers receive the message."""
        return message.get_topic().get_subscribers()


class RoundRobinMessageRoutingStrategy(MessageRoutingStrategy):
    def __init__(self):
        self.current_subscriber_index: int = 0

    def route(self, message: Message) -> List[MessageSubscriber]:
        """Round Robin: Routes to one subscriber at a time in round-robin fashion."""
        subscribers = message.get_topic().get_subscribers()
        if not subscribers:
            print(
                f"No subscribers found for topic {message.get_topic().get_name()} while routing message {message.get_id()} using RoundRobinMessageRoutingStrategy"
            )
            return []
        current_subscriber = subscribers[self.current_subscriber_index]
        self.current_subscriber_index = (self.current_subscriber_index + 1) % len(subscribers)
        return [current_subscriber]
