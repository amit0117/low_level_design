from app.models.enums import RideStatus
from app.models.location import Location
from app.models.payment_result import PaymentResult
from app.models.ride_state import RideState, RequestedState
from uuid import uuid4
from typing import Optional, TYPE_CHECKING
from app.observers.ride_observer import RideSubject

if TYPE_CHECKING:
    from app.models.rider import Rider
    from app.models.driver import Driver
    from app.models.user import User


class Ride(RideSubject):
    def __init__(
        self, rider: "Rider", driver: Optional["Driver"], pickup: Location, destination: Location, status: RideStatus, payment: PaymentResult
    ):
        super().__init__()
        self.id: str = str(uuid4())
        self.rider: "Rider" = rider
        self.driver: Optional["Driver"] = driver
        self.pickup: Location = pickup
        self.destination: Location = destination
        self.state: RideState = RequestedState()
        self.status: RideStatus = RideStatus.REQUESTED
        self.payment: PaymentResult = payment

    def get_id(self) -> str:
        return self.id

    def get_rider(self) -> "Rider":
        return self.rider

    def get_driver(self) -> Optional["Driver"]:
        return self.driver

    def get_pickup(self) -> Location:
        return self.pickup

    def get_destination(self) -> Location:
        return self.destination

    def get_status(self) -> RideStatus:
        return self.status

    def get_payment(self) -> PaymentResult:
        return self.payment

    def get_fare(self) -> float:
        return self.payment.get_amount()

    def set_driver(self, driver: "Driver") -> None:
        self.driver = driver

    def set_status(self, status: RideStatus) -> None:
        self.status = status
        # Notify observers whenever the status changes
        self.notify_observers(self)

    def set_state(self, state: RideState) -> None:
        self.state = state

    def set_payment(self, payment: PaymentResult) -> None:
        self.payment = payment

    # No need to add request_ride method because default state is RequestedState

    def accept_ride(self, driver: "Driver") -> None:
        self.state.accept_ride(self, driver)

    def start_ride(self) -> None:
        self.state.start_ride(self)

    def complete_ride(self) -> None:
        self.state.complete_ride(self)

    def cancel_ride(self, cancelled_by: "User") -> None:
        self.state.cancel_ride(self, cancelled_by)
