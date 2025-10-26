from uuid import uuid4
from datetime import datetime
from typing import Optional
from app.models.topic import Topic


class Message:
    def __init__(self, topic: Topic, payload: str, id: Optional[str] = None, timestamp: Optional[datetime] = None):
        self.id = id or str(uuid4())
        self.topic: Topic = topic
        self.timestamp: datetime = timestamp or datetime.now()
        self.payload: str = payload

    def get_topic(self) -> Topic:
        return self.topic

    def get_payload(self) -> str:
        return self.payload

    def get_timestamp(self) -> datetime:
        return self.timestamp

    def get_id(self) -> str:
        return self.id
