from uuid import uuid4
from app.observers.message_observer import MessageSubject
from app.models.subscriber import MessageSubscriber


class Topic(MessageSubject):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.id = str(uuid4())

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.id

    def get_subscribers(self) -> list[MessageSubscriber]:
        return self.observers.copy()

    def __eq__(self, other) -> bool:
        """Topics are equal if they have the same name."""
        if not isinstance(other, Topic):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        """Hash based on topic name for consistent dictionary lookups."""
        return hash(self.name)

    def __repr__(self) -> str:
        return f"Topic(id={self.id}, name={self.name})"
