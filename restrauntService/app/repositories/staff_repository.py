from typing import List, Optional
from threading import Lock
from app.models.staff import Manager, Chef, Waiter


class StaffRepository:
    """Repository for staff data access operations - Single Responsibility: Staff persistence"""

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
            self.managers: List[Manager] = []
            self.chefs: List[Chef] = []
            self.waiters: List[Waiter] = []
            self.data_lock = Lock()
            self._initialized = True

    def save_manager(self, manager: Manager) -> None:
        """Save manager to storage"""
        with self.data_lock:
            self.managers.append(manager)

    def save_chef(self, chef: Chef) -> None:
        """Save chef to storage"""
        with self.data_lock:
            self.chefs.append(chef)

    def save_waiter(self, waiter: Waiter) -> None:
        """Save waiter to storage"""
        with self.data_lock:
            self.waiters.append(waiter)

    def find_all_managers(self) -> List[Manager]:
        """Get all managers"""
        return self.managers.copy()

    def find_all_chefs(self) -> List[Chef]:
        """Get all chefs"""
        return self.chefs.copy()

    def find_all_waiters(self) -> List[Waiter]:
        """Get all waiters"""
        return self.waiters.copy()

    def find_chef_by_name(self, name: str) -> Optional[Chef]:
        """Find chef by name"""
        return next((chef for chef in self.chefs if chef.get_name() == name), None)

    def find_waiter_by_name(self, name: str) -> Optional[Waiter]:
        """Find waiter by name"""
        return next((waiter for waiter in self.waiters if waiter.get_name() == name), None)
