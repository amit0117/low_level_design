from datetime import datetime, timedelta
from app.models.bid import Bid
from typing import TYPE_CHECKING
from collections import defaultdict

if TYPE_CHECKING:
    from app.models.bid import Bid


class RateLimitProxy:
    def __init__(self, max_requests: int = 100, time_window: timedelta = timedelta(seconds=60)):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: dict[str, list[datetime]] = defaultdict(list)  # {user_id: [request_time]}

    def can_place_bid(self, bid: "Bid") -> bool:
        user_id = bid.get_user().get_id()

        # clean up the requests older than the time window
        for request_time in self.requests[user_id]:
            if request_time < datetime.now() - self.time_window:
                self.requests[user_id].remove(request_time)

        if len(self.requests[user_id]) >= self.max_requests:
            print(f"RateLimitProxy: User {user_id} has exceeded the rate limit")
            return False

        self.requests[user_id].append(datetime.now())
        return True
