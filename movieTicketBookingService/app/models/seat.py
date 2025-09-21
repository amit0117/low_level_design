from app.models.enums import SeatType, SeatStatus
import uuid


class Seat:
    def __init__(self, row: int, col: int, seat_type: SeatType):
        self._id = str(uuid.uuid4())
        self._row = row
        self._col = col
        self._seat_type = seat_type
        self._status = SeatStatus.AVAILABLE

    @property
    def id(self) -> str:
        return self._id

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col

    @property
    def type(self) -> SeatType:
        return self._seat_type

    @property
    def status(self) -> SeatStatus:
        return self._status

    def set_status(self, status: SeatStatus) -> None:
        self._status = status
