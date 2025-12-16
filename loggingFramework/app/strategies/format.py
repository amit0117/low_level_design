from abc import ABC, abstractmethod
from app.models.log_message import LogMessage
import json


class FormatStrategy(ABC):
    @abstractmethod
    def format(self, log_message: LogMessage) -> str:
        raise NotImplementedError("Subclasses must implement this method")


class TextFormatter(FormatStrategy):
    def format(self, log_message: LogMessage) -> str:
        return f"[{log_message.get_level().name}] {log_message.get_timestamp()} - {log_message.get_message()} - {log_message.get_thread_id() if log_message.get_thread_id() else ''}"


class JsonFormatter(FormatStrategy):
    def format(self, log_message: LogMessage) -> str:
        return json.dumps(
            {
                "level": log_message.get_level().name,
                "timestamp": log_message.get_timestamp(),
                "message": log_message.get_message(),
                "thread_id": log_message.get_thread_id() if log_message.get_thread_id() else "",
            }
        )
