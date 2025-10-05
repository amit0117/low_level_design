from app.models.borrow import Borrow
from app.models.library_item import LibraryItem
from app.models.member import Member
from app.models.payment_result import PaymentResult
from app.models.enums import BorrowStatus, ItemStatus, PaymentStatus
from app.repositories.borrow_repository import BorrowRepository
from app.repositories.item_repository import ItemRepository
from app.repositories.member_repository import MemberRepository
from app.services.payment_service import PaymentService
from app.strategies.payment_strategy import PaymentStrategy, CashPaymentStrategy
from datetime import datetime
from typing import Optional, List
from threading import Lock


class LibraryManagement:
    _lock = Lock()
    _instance: "LibraryManagement" = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self.borrow_repository = BorrowRepository.get_instance()
        self.item_repository = ItemRepository.get_instance()
        self.member_repository = MemberRepository.get_instance()
        self.payment_service = PaymentService()
        self.payment_service.set_payment_strategy(CashPaymentStrategy())  # default payment strategy is cash

        self.default_borrow_duration_days = 14
        self.max_renewals = 2
        self.daily_fine_amount = 1.0
        self.max_fine_amount = 50.0
        self._initialized = True

    @classmethod
    def get_instance(cls) -> "LibraryManagement":
        return cls._instance or cls()

    def register_member(self, name: str) -> Member:
        if not name or not name.strip():
            raise ValueError("Member name cannot be empty")
        existing_member = self.member_repository.get_member_by_name(name)
        if existing_member:
            raise ValueError(f"Member with name '{name}' already exists")
        member = Member(name.strip())
        self.member_repository.add_member(member)
        return member

    def add_item(self, item: LibraryItem) -> LibraryItem:
        self.item_repository.add_item(item)
        return item

    def request_item(self, item_id: str, member_id: str, duration_days: Optional[int] = None) -> Borrow:
        item = self.item_repository.get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item with ID '{item_id}' not found")
        member = self.member_repository.get_member_by_id(member_id)
        if not member:
            raise ValueError(f"Member with ID '{member_id}' not found")
        if item.get_status() != ItemStatus.AVAILABLE:
            raise ValueError(f"Item '{item.get_title()}' is not available")

        existing_borrows = self.borrow_repository.get_borrows_by_member(member)
        for borrow in existing_borrows:
            if borrow.get_item().get_id() == item_id and borrow.get_status() in [BorrowStatus.REQUESTED, BorrowStatus.ACTIVE]:
                raise ValueError(f"Member already has this item borrowed or requested")

        duration = duration_days or self.default_borrow_duration_days
        borrow = Borrow(item, member, duration)
        item.reserve(member)
        self.borrow_repository.add_borrow(borrow)
        return borrow

    def borrow_item(self, borrow_id: str) -> Borrow:
        borrow = self.borrow_repository.get_borrow_by_id(borrow_id)
        if not borrow:
            raise ValueError(f"Borrow request with ID '{borrow_id}' not found")
        if borrow.get_status() != BorrowStatus.REQUESTED:
            raise ValueError(f"Cannot borrow item. Current status: {borrow.get_status().value}")
        borrow.borrow()
        member = borrow.get_borrowed_by()
        member.add_to_borrow_history(borrow)
        return borrow

    def return_item(self, borrow_id: str) -> Borrow:
        borrow = self.borrow_repository.get_borrow_by_id(borrow_id)
        if not borrow:
            raise ValueError(f"Borrow record with ID '{borrow_id}' not found")
        if borrow.get_status() != BorrowStatus.ACTIVE:
            raise ValueError(f"Cannot return item. Current status: {borrow.get_status().value}")

        if self._is_overdue(borrow):
            fine_amount = self._calculate_fine(borrow)
            borrow.add_fine_amount(fine_amount)

        borrow.return_item()
        return borrow

    def renew_item(self, borrow_id: str, additional_days: Optional[int] = None) -> Borrow:
        borrow = self.borrow_repository.get_borrow_by_id(borrow_id)
        if not borrow:
            raise ValueError(f"Borrow record with ID '{borrow_id}' not found")
        if borrow.get_status() != BorrowStatus.ACTIVE:
            raise ValueError(f"Cannot renew item. Current status: {borrow.get_status().value}")
        if borrow.get_renewal_count() >= self.max_renewals:
            raise ValueError(f"Maximum renewals ({self.max_renewals}) exceeded")

        duration = additional_days or self.default_borrow_duration_days
        borrow.renew(duration)
        return borrow

    def cancel_request(self, borrow_id: str) -> Borrow:
        borrow = self.borrow_repository.get_borrow_by_id(borrow_id)
        if not borrow:
            raise ValueError(f"Borrow request with ID '{borrow_id}' not found")
        if borrow.get_status() != BorrowStatus.REQUESTED:
            raise ValueError(f"Cannot cancel request. Current status: {borrow.get_status().value}")
        borrow.cancel()
        return borrow

    def pay_fine(self, borrow_id: str, payment_strategy: Optional[PaymentStrategy] = None) -> PaymentResult:
        borrow = self.borrow_repository.get_borrow_by_id(borrow_id)
        if not borrow:
            raise ValueError(f"Borrow record with ID '{borrow_id}' not found")
        fine_amount = borrow.get_fine_amount()
        if fine_amount <= 0:
            raise ValueError("No fine amount to pay")

        if payment_strategy:
            self.payment_service.set_payment_strategy(payment_strategy)
        payment_result = self.payment_service.process_payment(fine_amount)

        if payment_result.get_status() == PaymentStatus.SUCCESS:
            borrow.fine_amount = 0
        return payment_result

    def pay_membership_fee(self, member_id: str, amount: float, payment_strategy: Optional[PaymentStrategy] = None) -> PaymentResult:
        member = self.member_repository.get_member_by_id(member_id)
        if not member:
            raise ValueError(f"Member with ID '{member_id}' not found")
        if amount <= 0:
            raise ValueError("Payment amount must be positive")

        if payment_strategy:
            self.payment_service.set_payment_strategy(payment_strategy)
        payment_result = self.payment_service.process_payment(amount)
        return payment_result

    def mark_item_lost(self, item_id: str) -> LibraryItem:
        item = self.item_repository.get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item with ID '{item_id}' not found")
        item.mark_lost()
        return item

    def mark_item_damaged(self, item_id: str) -> LibraryItem:
        item = self.item_repository.get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item with ID '{item_id}' not found")
        item.mark_damaged()
        return item

    def get_overdue_items(self) -> List[Borrow]:
        all_borrows = self.borrow_repository.get_all_borrows()
        return [borrow for borrow in all_borrows if borrow.get_status() == BorrowStatus.ACTIVE and self._is_overdue(borrow)]

    def get_member_fines(self, member_id: str) -> float:
        member = self.member_repository.get_member_by_id(member_id)
        if not member:
            raise ValueError(f"Member with ID '{member_id}' not found")
        member_borrows = self.borrow_repository.get_borrows_by_member(member)
        return sum(borrow.get_fine_amount() for borrow in member_borrows)

    def generate_library_report(self) -> dict:
        all_items = self.item_repository.get_all_items()
        all_members = self.member_repository.get_all_members()
        all_borrows = self.borrow_repository.get_all_borrows()

        item_status_counts = {}
        for status in ItemStatus:
            item_status_counts[status.value] = len([item for item in all_items if item.get_status() == status])

        borrow_status_counts = {}
        for status in BorrowStatus:
            borrow_status_counts[status.value] = len([borrow for borrow in all_borrows if borrow.get_status() == status])

        total_fines = sum(borrow.get_fine_amount() for borrow in all_borrows)

        return {
            "total_items": len(all_items),
            "total_members": len(all_members),
            "total_borrows": len(all_borrows),
            "item_status_breakdown": item_status_counts,
            "borrow_status_breakdown": borrow_status_counts,
            "total_fines": total_fines,
            "overdue_items": len(self.get_overdue_items()),
        }

    def _is_overdue(self, borrow: Borrow) -> bool:
        if borrow.get_status() != BorrowStatus.ACTIVE:
            return False
        due_date = borrow.get_due_date()
        return datetime.now() > due_date

    def _calculate_fine(self, borrow: Borrow) -> float:
        if not self._is_overdue(borrow):
            return 0.0
        due_date = borrow.get_due_date()
        days_overdue = (datetime.now() - due_date).days
        fine_amount = days_overdue * self.daily_fine_amount
        return min(fine_amount, self.max_fine_amount)
