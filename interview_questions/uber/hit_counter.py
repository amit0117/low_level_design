# Design Hit Counter For concurrent Approach
#
# Q) Design a hit counter which counts the number of hits received in the past 5 minutes.
#    Each function accepts a timestamp parameter (in seconds granularity) and you may assume that
#    calls are being made to the system in chronological order (ie, the timestamp is monotonically increasing).
#    You may assume that the earliest timestamp starts at 1. It is possible that several hits arrive roughly at the same time.
# Follow up:
#    What if the number of hits per second could be very large? Does your design scale?
#
# Approach 1: use queue to add the new requests and when getHit request comes then delete the entries with time > 5 minutes and return len(queue).
# We can use queue (we will use deque to implement queue)
# we can use queue from Queue but for get and put are blocking request , also we if we decided to use get_nowait() and put_nowait(), then we need to handle Empty and Full Exception respectively

from collections import deque
from threading import Lock


class HitCounter:
    def __init__(self, window_in_min: int = 5):
        # we will play with seconds , because timestamp are in seconds
        self.window = window_in_min * 60
        self.dq = deque()

    def _cleanup(self, timestamp: int) -> None:
        while len(self.dq) > 0 and self.dq[0] - timestamp > self.window:
            self.dq.popleft()

    def hit(self, timestamp: int) -> None:
        self.dq.append(timestamp)
        self._cleanup(timestamp)

    def getHits(self, timestamp: int) -> int:
        self._cleanup(timestamp)
        return len(self.dq)


# Queue works but is not optimal because it stores every hit, leading to high memory usage and occasional O(n) cleanup.

# Second solution: Circulat buffer aggreates hits per Second
class HitCounterOptimised:
    def __init__(self, window_in_min: int = 5):
        self.window = window_in_min * 60
        # This will act as the circular array and will store the actual timestamp for each timestamp%window
        self.timestamps = [0] * self.window
        self.hit_fre = [0] * self.window

    def hit(self, timestamp: int) -> None:
        timestamp_with_mod = timestamp % self.window

        if self.timestamps[timestamp_with_mod] != timestamp:
            # it means the previous window has expired, So the previous hit count will not contibute further.
            # So we have to remove those, And we will add fre as 1 for current visit and update it's value in timestamps
            self.timestamps[timestamp_with_mod] = timestamp
            self.hit_fre[timestamp_with_mod] = 1
        else:
            # current timestamp is in the same window, So we can increase it's count
            self.hit_fre[timestamp_with_mod] += 1

    def getHits(self, timestamp: int) -> int:

        res = 0
        for index in range(self.window):
            # only add it's hit_fre value if this is in current window
            # how to decide if the current timestamp (_timestamp) is in current window
            # we can check if timestamp-_timestamp < window , because in worst case we will calculate when timestamp is the next window Second
            # for example, for 5 minutes, window is 300,
            # suppose timestamps         [0,1,2,3,....,299] -> here 0 will encounter for timestamp = 300
            # timestamp values will be [300,1,2,3,...,299] ->
            # Now suppose, current timestamp is 303
            # we need to exclude timestamp 1,2 and 3. So we will only use the value where curr_timestamp - timestamps[i] < 300
            if timestamp - self.timestamps[index] < self.window:
                res += self.hit_fre[index]

        return res


# Now this solution is sacalable with Constant time and space
# But we still have concurency issue here,
# There are several places where race condition can happen , like
# in hit [if timestamps[timestamp_with_mod]!=timestamp:] ,[self.hit_fre[timestamp_with_mod]+=1 -> this is also not atomic]

# Solution:
# a) Use Global Lock and use before each hit and getHits operation, This will ensure correctness but contention will be high
# b) Use lock per bucket/timestamp for better concurrency


class ThreadSafeHitCounter:
    def __init__(self, window_in_min: 5):
        self.window = window_in_min * 60
        self.times = [0] * self.window
        self.hits = [0] * self.window
        self.locks = [Lock() for _ in range(self.window)]

    def hit(self, timestamp: int) -> None:
        timestamp_idx = timestamp % self.window
        # Only use the specific lock, by doing this other hit and getHits call won't be blocked
        with self.locks[timestamp_idx]:
            if self.times[timestamp_idx] != timestamp:
                self.times[timestamp_idx] = timestamp
                self.hits[timestamp_idx] = 1
            else:
                self.hits[timestamp_idx] += 1

    def getHits(self, timestamp: int) -> int:
        total = 0
        for i in range(self.window):
            with self.locks[i]:
                if timestamp - self.times[i] < self.window:
                    total += self.hits[i]
        return total
