from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
from uuid import uuid4
from app.models.enums import CommandStatus


class Command(ABC):
    def __init__(self):
        self.command_id = str(uuid4())
        self.status = CommandStatus.PENDING
        self.created_at = datetime.now()
        self.executed_at: Optional[datetime] = None
        self.error_message: Optional[str] = None
        self.retry_count = 0
        self.max_retries = 3

    @abstractmethod
    def execute(self) -> bool:
        """Execute the command. Returns True if successful, False otherwise."""
        raise NotImplementedError("execute method must be implemented")

    @abstractmethod
    def undo(self) -> bool:
        """Undo the command. Returns True if successful, False otherwise."""
        raise NotImplementedError("undo method must be implemented")

    def get_command_id(self) -> str:
        return self.command_id

    def get_status(self) -> CommandStatus:
        return self.status

    def set_status(self, status: CommandStatus) -> None:
        self.status = status
        if status == CommandStatus.COMPLETED:
            self.executed_at = datetime.now()

    def set_error(self, error_message: str) -> None:
        self.error_message = error_message


    def increment_retry(self) -> None:
        self.retry_count += 1

    def can_retry(self) -> bool:
        return self.retry_count < self.max_retries and self.status == CommandStatus.FAILED

    def get_execution_time(self) -> Optional[float]:
        if self.executed_at:
            return (self.executed_at - self.created_at).total_seconds()
        return None
