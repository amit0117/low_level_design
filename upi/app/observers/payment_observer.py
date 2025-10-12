from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.payment import Payment


class PaymentObserver(ABC):

    @abstractmethod
    def update_on_payment(self, payment: "Payment") -> None:
        raise NotImplementedError("update_on_payment method must be implemented")


class PaymentSubject:
    def __init__(self):
        self.observers: list[PaymentObserver] = []

    def add_observer(self, observer: PaymentObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: PaymentObserver) -> None:
        self.observers.remove(observer)

    def notify_observers(self, payment: "Payment") -> None:
        print(f"Notifying {len(self.observers)} observers about payment {payment.get_payment_id()}")
        for observer in self.observers:
            observer.update_on_payment(payment)
