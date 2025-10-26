from abc import ABC, abstractmethod
from app.models.message import Message
from typing import Optional
from datetime import datetime
from threading import Lock, Condition
from collections import deque


class MessageQueueStrategy(ABC):
    @abstractmethod
    def enqueue(self, message: Message):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def dequeue(self) -> Message:
        raise NotImplementedError("Subclasses must implement this method")


class inMemoryMessageQueueStrategy(MessageQueueStrategy):
    def __init__(self):
        self.message_queue: deque[Message] = deque()
        self.lock = Lock()
        self.condition = Condition(self.lock)  # Condition variable is used when consumer is pull based like Kafka
        self._stopped = False  # Flag to indicate when queue should stop

    def stop(self):
        """Mark the queue as stopped to allow clean shutdown."""
        with self.condition:
            self._stopped = True
            self.condition.notify_all()

    def enqueue(self, message: Message):
        with self.condition:
            self.message_queue.appendleft(message)
            self.condition.notify_all()

    def dequeue(self) -> Message:
        with self.condition:
            while not self.message_queue and not self._stopped:
                self.condition.wait()
            if self._stopped:
                raise RuntimeError("Queue has been stopped")
            return self.message_queue.pop()


class fileMessageQueueStrategy(MessageQueueStrategy):
    def __init__(self, filename: Optional[str] = None):
        self.filename = filename or "message_queue.txt"
        self.lock = Lock()
        # simplistic persistent storage simulation
        open(self.filename, "a").close()

    def enqueue(self, message: Message):
        with self.lock:
            with open(self.filename, "a") as f:
                f.write(f"{message.get_id()}:{message.get_topic()}:{message.get_payload()}:{message.get_timestamp().strftime('%Y-%m-%d %H:%M:%S')}\n")

    def dequeue(self) -> Message:
        with self.lock:
            lines: list[str] = []
            with open(self.filename, "r") as f:
                lines = f.readlines()
            if not lines:
                raise ValueError("Queue is empty")
            first_line = lines[0]
            message_id, topic, payload, timestamp = first_line.split(":")  # At a time only one message is returned
            with open(self.filename, "w") as f:  # Remove the first line from the file and write the remaining lines back to the file
                f.writelines(lines[1:])
            return Message(topic, payload, id=message_id, timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
