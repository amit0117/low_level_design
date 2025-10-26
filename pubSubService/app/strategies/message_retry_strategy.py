import time
import random
from abc import ABC, abstractmethod
from app.models.message import Message
from collections.abc import Callable


# ---- Base Retry Strategy Interface ----
class MessageRetryStrategy(ABC):
    @abstractmethod
    def retry(self, func: Callable[[Message], None], message: Message) -> bool:
        raise NotImplementedError("Subclasses must implement this method")


# ---- 1️⃣ Fixed Interval Retry ----
class FixedIntervalRetry(MessageRetryStrategy):
    def __init__(self, retries=3, interval=2):
        self.retries_count = retries
        self.interval = interval

    def retry(self, func: Callable[[Message], None], message: Message) -> bool:
        for attempt in range(1, self.retries_count + 1):
            try:
                func(message)
                return True
            except Exception as e:
                time.sleep(self.interval)
        return False


# ---- 2️⃣ Exponential Backoff Retry ----
class ExponentialBackoffRetry(MessageRetryStrategy):
    def __init__(self, retries=2, base_delay=1, max_delay=16):
        self.retries_count = retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def retry(self, func: Callable[[Message], None], message: Message) -> bool:
        for attempt in range(1, self.retries_count + 1):
            try:
                func(message)
                return True
            except Exception as e:
                delay = min(self.base_delay * (2 ** (attempt - 1)), self.max_delay)
                time.sleep(delay)
        return False


# ---- 3️⃣ Jitter (Randomized Backoff) Retry ----
class JitterRetry(MessageRetryStrategy):
    def __init__(self, retries=5, base_delay=1, max_delay=10):
        self.retries_count = retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def retry(self, func: Callable[[Message], None], message: Message) -> bool:
        for attempt in range(1, self.retries_count + 1):
            try:
                func(message)
                return True
            except Exception as e:
                delay = random.uniform(self.base_delay, self.max_delay)
                time.sleep(delay)
        return False


# ---- 4️⃣ No Retry (At Most Once) ----
class NoRetry(MessageRetryStrategy):
    def retry(self, func: Callable[[Message], None], message: Message) -> bool:
        try:
            func(message)
            return True
        except Exception as e:
            return False
