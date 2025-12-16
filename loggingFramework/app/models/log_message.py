from app.models.enums import LogLevel
from datetime import datetime
from typing import Optional
import threading


class LogMessage:
    def __init__(self, level: LogLevel, message: str):
        self.level = level
        self.message = message
        self.timestamp = datetime.now()
        self.thread_id = threading.get_ident()
        # Context variable (from contextvars import ContextVar) is used to manage the thread id for logger because the process might context switch to different threads and we might log inconsistent thread ids in the log file
        # Any other variable we may log here (like RequestId,userId,etc.) can be added here similar to thread_id

    def get_level(self) -> LogLevel:
        return self.level

    def get_message(self) -> str:
        return self.message

    def get_thread_id(self) -> Optional[str]:
        return self.thread_id

    def get_timestamp(self) -> datetime:
        return self.timestamp

    def __str__(self) -> str:
        return f"[{self.level}] {self.timestamp} - {self.message} - {self.thread_id if self.thread_id else ''}"
