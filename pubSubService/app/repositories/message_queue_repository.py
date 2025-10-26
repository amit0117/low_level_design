"""
Message Queue Repository - Singleton pattern with double-checked locking
Manages all message queues in the pub-sub system
"""

from app.models.message_queue import MessageQueue
import threading
from typing import Optional, Dict


class MessageQueueRepository:
    """Singleton repository for managing message queues."""

    _instance: Optional["MessageQueueRepository"] = None
    _lock = threading.Lock()

    def __new__(cls):
        """Double-checked locking singleton implementation."""
        if cls._instance is None:  # First check (no lock)
            with cls._lock:
                if cls._instance is None:  # Second check (with lock)
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize repository (called only once due to singleton)."""
        if self._initialized:
            return
        self._queues: Dict[str, MessageQueue] = {}
        self._lock = threading.Lock()
        self._initialized = True

    def add_queue(self, queue_id: str, queue: MessageQueue) -> bool:
        """Add a queue to the repository."""
        with self._lock:
            if queue_id in self._queues:
                return False
            self._queues[queue_id] = queue
            return True

    def get_queue(self, queue_id: str) -> Optional[MessageQueue]:
        """Get queue by ID."""
        with self._lock:
            return self._queues.get(queue_id)

    def remove_queue(self, queue_id: str) -> bool:
        """Remove a queue from the repository."""
        with self._lock:
            if queue_id in self._queues:
                del self._queues[queue_id]
                return True
            return False

    def get_all_queues(self) -> list[MessageQueue]:
        """Get all queues."""
        with self._lock:
            return list(self._queues.values())

    def queue_exists(self, queue_id: str) -> bool:
        """Check if queue exists."""
        with self._lock:
            return queue_id in self._queues

    def get_count(self) -> int:
        """Get total number of queues."""
        with self._lock:
            return len(self._queues)

    def clear(self) -> None:
        """Clear all queues."""
        with self._lock:
            self._queues.clear()


# Global instance accessor
def get_message_queue_repository() -> MessageQueueRepository:
    """Get the singleton message queue repository instance."""
    return MessageQueueRepository()
