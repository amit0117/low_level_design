from app.models.enums import TableStatus
from app.states.table_state import AvailableTableState, TableState
from app.observers.table_observer import TableSubject


class Table(TableSubject):
    def __init__(self, table_number: int, capacity: int) -> None:
        super().__init__()
        self.table_number = table_number
        self.capacity = capacity
        self.status = TableStatus.AVAILABLE
        self.state = AvailableTableState()

    def get_table_number(self) -> int:
        return self.table_number

    def get_capacity(self) -> int:
        return self.capacity

    def get_status(self) -> TableStatus:
        return self.status

    def get_state(self) -> TableState:
        return self.state

    def set_status(self, status: TableStatus) -> None:
        self.status = status
        self.notify_observers(self)

    def set_state(self, state: TableState) -> None:
        self.state = state

    def display_table_info(self) -> None:
        self.state.display_table_info(self)

    def reserve_table(self) -> None:
        self.state.reserve_table(self)

    def release_table(self) -> None:
        self.state.release_table(self)

    def occupy_table(self) -> None:
        self.state.occupy_table(self)

    def is_available(self) -> bool:
        return self.status == TableStatus.AVAILABLE

    def is_occupied(self) -> bool:
        return self.status == TableStatus.OCCUPIED

    def is_reserved(self) -> bool:
        return self.status == TableStatus.RESERVED
