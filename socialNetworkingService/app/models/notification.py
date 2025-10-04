from datetime import datetime
from app.models.enums import NotificationType


class Notification:
    def __init__(self, message: str, type: NotificationType):
        self.message = message
        self.type = type
        self.created_at = datetime.now()
        self.is_read = False

    def get_message(self) -> str:
        return self.message

    def get_type(self) -> NotificationType:
        return self.type

    def get_created_at(self) -> datetime:
        return self.created_at

    def is_read(self) -> bool:
        return self.is_read

    def mark_as_read(self) -> None:
        self.is_read = True
