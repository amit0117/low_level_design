from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from app.adapters.base_adapter import StandardizedResponse

if TYPE_CHECKING:
    from app.models.payment import Payment


class PaymentHandler(ABC):
    """Base handler for Chain of Responsibility pattern"""

    def __init__(self):
        self._next_handler: Optional["PaymentHandler"] = None

    def set_next(self, handler: "PaymentHandler") -> "PaymentHandler":
        """Set the next handler in the chain"""
        self._next_handler = handler
        return handler

    def handle(self, payment: "Payment") -> StandardizedResponse:
        """Handle payment or pass to next handler"""

        # Process current handler
        response = self._process(payment)

        # If current handler failed, return failure
        if not response.success:
            return response

        # If there's a next handler, pass to it
        if self._next_handler:
            return self._next_handler.handle(payment)

        # No more handlers, return success
        return response

    @abstractmethod
    def _process(self, payment: "Payment") -> StandardizedResponse:
        """Process payment in this handler"""
        raise NotImplementedError

    def get_handler_name(self) -> str:
        """Get handler name for logging/debugging"""
        return self.__class__.__name__
