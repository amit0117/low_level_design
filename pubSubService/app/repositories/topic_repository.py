"""
Topic Repository - Singleton pattern with double-checked locking
Manages all topics in the pub-sub system
"""

from app.models.topic import Topic
import threading
from typing import Optional, Dict


class TopicRepository:
    """Singleton repository for managing topics."""

    _instance: Optional["TopicRepository"] = None
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
        self._topics: Dict[str, Topic] = {}
        self._lock = threading.Lock()
        self._initialized = True

    def add_topic(self, topic: Topic) -> bool:
        """Add a topic to the repository."""
        with self._lock:
            if topic.get_id() in self._topics:
                return False
            self._topics[topic.get_id()] = topic
            return True

    def get_topic(self, topic_id: str) -> Optional[Topic]:
        """Get topic by ID."""
        with self._lock:
            return self._topics.get(topic_id)

    def get_topic_by_name(self, topic_name: str) -> Optional[Topic]:
        """Get topic by name."""
        with self._lock:
            for topic in self._topics.values():
                if topic.get_name() == topic_name:
                    return topic
            return None

    def remove_topic(self, topic_id: str) -> bool:
        """Remove a topic from the repository."""
        with self._lock:
            if topic_id in self._topics:
                del self._topics[topic_id]
                return True
            return False

    def get_all_topics(self) -> list[Topic]:
        """Get all topics."""
        with self._lock:
            return list(self._topics.values())

    def topic_exists(self, topic_id: str) -> bool:
        """Check if topic exists."""
        with self._lock:
            return topic_id in self._topics

    def get_count(self) -> int:
        """Get total number of topics."""
        with self._lock:
            return len(self._topics)

    def clear(self) -> None:
        """Clear all topics."""
        with self._lock:
            self._topics.clear()


# Global instance accessor
def get_topic_repository() -> TopicRepository:
    """Get the singleton topic repository instance."""
    return TopicRepository()
