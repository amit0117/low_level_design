from typing import Optional, List
from app.repositories.staff_repository import StaffRepository
from app.models.staff import Chef, Waiter, Manager
from app.models.staff import Staff
from app.models.enums import StaffRole


class StaffService:
    def __init__(self):
        self.staff_repo = StaffRepository()

    def add_staff_member(self, staff_member: Staff) -> None:
        if hasattr(staff_member, "get_role"):
            role = staff_member.get_role()
            if role.value == StaffRole.MANAGER.value:
                self.staff_repo.save_manager(staff_member)
            elif role.value == StaffRole.CHEF.value:
                self.staff_repo.save_chef(staff_member)
            elif role.value == StaffRole.WAITER.value:
                self.staff_repo.save_waiter(staff_member)
            else:
                raise ValueError(f"Unknown staff role: {role}")
        else:
            raise ValueError("Invalid staff member")

    def get_all_chefs(self) -> List[Chef]:
        return self.staff_repo.find_all_chefs()

    def get_all_waiters(self) -> List[Waiter]:
        return self.staff_repo.find_all_waiters()

    def get_all_managers(self) -> List[Manager]:
        return self.staff_repo.find_all_managers()

    def get_available_chef(self) -> Optional[Chef]:
        chefs = self.staff_repo.find_all_chefs()
        return chefs[0] if chefs else None

    def get_available_waiter(self) -> Optional[Waiter]:
        waiters = self.staff_repo.find_all_waiters()
        return waiters[0] if waiters else None

    def get_staff_status(self) -> dict:
        return {
            "managers": len(self.staff_repo.find_all_managers()),
            "chefs": len(self.staff_repo.find_all_chefs()),
            "waiters": len(self.staff_repo.find_all_waiters()),
        }
