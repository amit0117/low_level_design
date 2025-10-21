from app.observers.elevator_observer import ElevatorObserver
from typing import Any, override


class DisplayPanel(ElevatorObserver):
    def __init__(self, content: str) -> None:
        ElevatorObserver.__init__(self)
        self.content = content

    def get_content(self) -> str:
        return self.content

    def update_content(self, updated_content: str) -> None:
        self.content = updated_content

    @override
    def update(self, *args: Any, **kwargs: dict) -> None:
        message = args[0]
        self.update_content(message)
        print(f"[DISPLAY PANEL]: {self.get_content()}")
