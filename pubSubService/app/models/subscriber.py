from app.observers.message_observer import MessageObserver
from uuid import uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.message import Message
    from app.models.topic import Topic


class MessageSubscriber(MessageObserver):
    def __init__(self, name: str):
        super().__init__()
        self.subscriber_id = str(uuid4())
        self.name = name
        self.subscribed_topics: list["Topic"] = []

    def get_name(self) -> str:
        return self.name

    def get_subscribed_topics(self) -> list["Topic"]:
        return self.subscribed_topics.copy()

    def subscribe_to_topic(self, topic: "Topic") -> None:
        if topic not in self.subscribed_topics:
            self.subscribed_topics.append(topic)
            topic.subscribe(self)

    def unsubscribe_from_topic(self, topic: "Topic") -> None:
        if topic in self.subscribed_topics:
            self.subscribed_topics.remove(topic)
            topic.unsubscribe(self)

    def receive(self, message: "Message") -> None:
        print(f"📨 {self.name}: {message.get_payload()}")

    def acknowledge(self, message: "Message") -> bool:
        # Message acknowledged silently
        return True
