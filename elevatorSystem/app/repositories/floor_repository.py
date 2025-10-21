from threading import Lock
from app.models.floor import Floor


class FloorRepository:
    _instance: "FloorRepository" = None
    _lock: Lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_floors"):
            return
        self._floors: dict[int, Floor] = dict()

    @classmethod
    def get_instance(cls) -> "FloorRepository":
        return cls._instance or cls()

    def save(self, floor: Floor) -> None:
        with self._lock:
            self._floors.setdefault(floor.get_floor_number(), floor)

    def find_by_floor_number(self, floor_number: int) -> Floor:
        if floor_number in self._floors:
            return self._floors[floor_number]
        return None

    def get_all_floors(self) -> list[Floor]:
        return list(self._floors.values())
