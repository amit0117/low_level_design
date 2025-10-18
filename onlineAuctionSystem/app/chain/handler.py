from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timedelta
from collections import defaultdict

if TYPE_CHECKING:
    from app.models.user import User


class AuctionRequest:

    def __init__(self, user: "User", password: str):
        self.user = user
        self.password = password
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


class AuthenticationHandler(BaseAuctionHandler):
    def __init__(self):
        super().__init__()

    def handle(self, request: AuctionRequest) -> bool:
        if not request.user.is_valid_password(request.password):
            return False
        return super().handle(request)


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
            print(f"Rate limit exceeded for user {request.user.get_name()}. " f"Max {self.max_requests_per_minute} requests per minute.")
            return False

        self.user_requests[user_id].append(current_time)

        print(f"Rate limit check passed for user {request.user.get_name()}")

        return super().handle(request)


class AuctionChainBuilder:

    @staticmethod
    def create_auction_processing_chain() -> AuctionHandler:
        authentication_handler = AuthenticationHandler()
        rate_limit_handler = RateLimitHandler(max_requests_per_minute=5)

        authentication_handler.set_next(rate_limit_handler)

        return authentication_handler
