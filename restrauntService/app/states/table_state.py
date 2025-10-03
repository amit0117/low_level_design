from abc import ABC, abstractmethod
from app.models.enums import TableStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.table import Table


class TableState(ABC):
    @abstractmethod
    def reserve_table(self, table: "Table") -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def release_table(self, table: "Table") -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def occupy_table(self, table: "Table") -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def display_table_info(self, table: "Table") -> None:
        raise NotImplementedError("Subclasses must implement this method")


class AvailableTableState(TableState):
    def reserve_table(self, table: "Table") -> None:
        table.set_state(ReservedTableState())
        table.set_status(TableStatus.RESERVED)

    def release_table(self, table: "Table") -> None:
        print("Table is already available")

    def occupy_table(self, table: "Table") -> None:
        print("Can't occupy this table . First reserve it")

    def display_table_info(self, table: "Table") -> None:
        print(f"Table {table.get_table_number()} is available")


class ReservedTableState(TableState):
    def reserve_table(self, table: "Table") -> None:
        print("Table is already reserved")

    def release_table(self, table: "Table") -> None:
        table.set_state(AvailableTableState())
        table.set_status(TableStatus.AVAILABLE)

    def occupy_table(self, table: "Table") -> None:
        table.set_state(OccupiedTableState())
        table.set_status(TableStatus.OCCUPIED)

    def display_table_info(self, table: "Table") -> None:
        print(f"Table {table.get_table_number()} is reserved")


class OccupiedTableState(TableState):
    def reserve_table(self, table: "Table") -> None:
        print("Table is already occupied")

    def release_table(self, table: "Table") -> None:
        table.set_state(AvailableTableState())
        table.set_status(TableStatus.AVAILABLE)

    def occupy_table(self, table: "Table") -> None:
        print("Table is already occupied")

    def display_table_info(self, table: "Table") -> None:
        print(f"Table {table.get_table_number()} is occupied")
