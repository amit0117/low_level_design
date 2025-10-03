from typing import List
from app.repositories.table_repository import TableRepository
from app.models.table import Table


class TableService:
    def __init__(self):
        self.table_repo = TableRepository()

    def add_table(self, table: Table) -> None:
        self.table_repo.save(table)

    def reserve_table(self, table_number: int, customer_name: str, group_size: int) -> bool:
        table = self.table_repo.find_by_id(table_number)

        if not table:
            print(f"Table {table_number} not found")
            return False

        if not table.is_available():
            print(f"Table {table_number} is not available")
            return False

        if group_size > table.get_capacity():
            print(f"Group size {group_size} exceeds table capacity {table.get_capacity()}")
            return False

        table.reserve_table()
        self.table_repo.update(table)

        print(f"Table {table_number} reserved for {customer_name}")
        return True

    def occupy_table(self, table_number: int) -> bool:
        table = self.table_repo.find_by_id(table_number)

        if not table:
            print(f"Table {table_number} not found")
            return False

        if not (table.is_available() or table.is_reserved()):
            print(f"Table {table_number} cannot be occupied")
            return False

        table.occupy_table()
        self.table_repo.update(table)

        print(f"Table {table_number} is now occupied")
        return True

    def release_table(self, table_number: int) -> bool:
        table = self.table_repo.find_by_id(table_number)

        if not table:
            print(f"Table {table_number} not found")
            return False

        if not table.is_occupied():
            print(f"Table {table_number} is not occupied")
            return False

        table.release_table()
        self.table_repo.update(table)

        print(f"Table {table_number} is now available")
        return True

    def get_available_tables(self) -> List[Table]:
        return self.table_repo.find_available()

    def get_all_tables(self) -> List[Table]:
        return self.table_repo.find_all()

    def get_table_status(self) -> dict:
        tables = self.table_repo.find_all()
        return {
            "total": len(tables),
            "available": len(self.table_repo.find_available()),
            "occupied": len(self.table_repo.find_occupied()),
            "reserved": len(self.table_repo.find_reserved()),
        }
