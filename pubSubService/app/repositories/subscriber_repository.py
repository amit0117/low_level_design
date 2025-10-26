from app.models.subscriber import MessageSubscriber
import threading
from typing import Optional, Dict


class SubscriberRepository:
    _instance: Optional["SubscriberRepository"] = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._subscribers: Dict[str, MessageSubscriber] = {}
        self._lock = threading.Lock()
        self._initialized = True

    def add_subscriber(self, subscriber: MessageSubscriber) -> bool:
        with self._lock:
            if subscriber.subscriber_id in self._subscribers:
                return False
            self._subscribers[subscriber.subscriber_id] = subscriber
            return True

    def get_subscriber(self, subscriber_id: str) -> Optional[MessageSubscriber]:
        with self._lock:
            return self._subscribers.get(subscriber_id)

    def remove_subscriber(self, subscriber_id: str) -> bool:
        with self._lock:
            if subscriber_id in self._subscribers:
                del self._subscribers[subscriber_id]
                return True
            return False

    def get_all_subscribers(self) -> list[MessageSubscriber]:
        with self._lock:
            return list(self._subscribers.values())


def get_subscriber_repository() -> SubscriberRepository:
    return SubscriberRepository()
