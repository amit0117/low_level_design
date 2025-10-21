from app.observers.base_observer import Observer


class ElevatorObserver(Observer):
    def update(self, message: str) -> None:
        print(f"[ELEVATOR OBSERVER]: {message}")
