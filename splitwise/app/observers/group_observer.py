from app.observers.base_observer import Subject


class GroupSubject(Subject):
    """Subject for group-related notifications"""

    def notify_observers(self, message: str = "") -> None:
        for observer in self._observers:
            observer.update_group(message)
