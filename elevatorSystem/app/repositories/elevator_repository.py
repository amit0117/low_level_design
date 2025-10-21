from threading import Lock
from app.models.elevator import Elevator


class ElevatorRepository:
    _instance: "ElevatorRepository" = None
    _lock: Lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_elevators"):
            return
        self._elevators: dict[str, Elevator] = dict()

    @classmethod
    def get_instance(cls) -> "ElevatorRepository":
        return cls._instance or cls()

    def save(self, elevator: Elevator) -> None:
        with self._lock:
            self._elevators.setdefault(elevator.get_id(), elevator)

    def find_by_id(self, elevator_id: str) -> Elevator:
        return self._elevators.get(elevator_id)

    def get_all_elevators(self) -> list[Elevator]:
        return list(self._elevators.values())
