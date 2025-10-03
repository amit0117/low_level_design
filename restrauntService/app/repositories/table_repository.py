from typing import List, Optional, Dict
from threading import Lock
from app.models.table import Table


class TableRepository:
    """Repository for table data access operations - Single Responsibility: Table persistence"""

    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.tables: Dict[int, Table] = {}
            self.data_lock = Lock()
            self._initialized = True

    def save(self, table: Table) -> None:
        """Save table to storage"""
        with self.data_lock:
            self.tables[table.get_table_number()] = table

    def find_by_id(self, table_id: int) -> Optional[Table]:
        """Find table by ID"""
        return self.tables.get(table_id)

    def find_all(self) -> List[Table]:
        """Get all tables"""
        return list(self.tables.values())

    def find_available(self) -> List[Table]:
        """Get all available tables"""
        return [table for table in self.tables.values() if table.is_available()]

    def find_occupied(self) -> List[Table]:
        """Get all occupied tables"""
        return [table for table in self.tables.values() if table.is_occupied()]

    def find_reserved(self) -> List[Table]:
        """Get all reserved tables"""
        return [table for table in self.tables.values() if table.is_reserved()]

    def update(self, table: Table) -> None:
        """Update table in storage"""
        with self.data_lock:
            self.tables[table.get_table_number()] = table

    def delete(self, table_id: int) -> bool:
        """Delete table from storage"""
        with self.data_lock:
            if table_id in self.tables:
                del self.tables[table_id]
                return True
            return False
