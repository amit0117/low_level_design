from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timedelta
from collections import defaultdict

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.bid import Bid


class AuctionRequest:
    def __init__(self, bid: "Bid", user: "User", request_type: str):
        self.bid = bid
        self.user = user
        self.request_type = request_type
        self.timestamp = datetime.now()


class AuctionHandler(ABC):
    @abstractmethod
    def handle(self, request: AuctionRequest) -> bool:
        raise NotImplementedError("Handle method has not been implemented")

    @abstractmethod
    def set_next(self, handler: "AuctionHandler") -> "AuctionHandler":
        raise NotImplementedError("Set next method has not been implemented")


class BaseAuctionHandler(AuctionHandler):
    def __init__(self):
        self.next_handler: Optional[AuctionHandler] = None

    def handle(self, request: AuctionRequest) -> bool:
        if self.next_handler:
            return self.next_handler.handle(request)
        return True

    def set_next(self, handler: AuctionHandler) -> AuctionHandler:
        self.next_handler = handler
        return handler


class RateLimitHandler(BaseAuctionHandler):
    def __init__(self, max_requests_per_minute: int = 10):
        super().__init__()
        self.max_requests_per_minute = max_requests_per_minute
        self.user_requests: dict[str, list[datetime]] = defaultdict(list)

    def handle(self, request: AuctionRequest) -> bool:
        user_id = request.user.get_id()
        current_time = datetime.now()

        minute_ago = current_time - timedelta(minutes=1)
        self.user_requests[user_id] = [req_time for req_time in self.user_requests[user_id] if req_time > minute_ago]

        if len(self.user_requests[user_id]) >= self.max_requests_per_minute:
            print(f"Rate limit exceeded for user {request.user.get_name()}. Max {self.max_requests_per_minute} requests per minute.")
            return False

        self.user_requests[user_id].append(current_time)
        print(f"Rate limit check passed for user {request.user.get_name()}")

        return super().handle(request)


class ValidationHandler(BaseAuctionHandler):
    def handle(self, request: AuctionRequest) -> bool:
        auction = request.bid.get_auction()

        if not auction.can_place_bid(request.bid):
            print(f"Validation failed for bid by {request.user.get_name()}")
            return False

        print(f"Validation passed for bid by {request.user.get_name()}")
        return super().handle(request)


class AuctionChainBuilder:
    @staticmethod
    def create_bid_processing_chain() -> AuctionHandler:
        rate_limit_handler = RateLimitHandler(max_requests_per_minute=5)
        validation_handler = ValidationHandler()

        rate_limit_handler.set_next(validation_handler)
        return rate_limit_handler
