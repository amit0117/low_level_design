from contextlib import contextmanager
from threading import Lock
from collections import defaultdict
from typing import Generator

# Lock manager will be used to manage locks of all parking spots of a level
# Why this is needed?
# What if we go for each lock per Level?
# Concurrency is very less, eg if 10 request for same floor is there we can only process a single request at a time because of level lock

# What if we go for each lock per ParkingSpot?
# We pre-create and maintain a lock for every spot globally.
# Even if 90% of spots are empty or rarely used, their locks sit in memory.
# A per-spot lock gives maximum concurrency but creates thousands of locks to maintain, leading to high memory use and complex synchronization

# So, we need to find a way to manage locks of all parking spots of a level in a single lock
# This is where LockManager comes into play

# How LockManager works?
# The hybrid approach dynamically creates and manages locks per spot within each floor’s LockManager, achieving fine-grained concurrency
#   while keeping lock management localized and lightweight
#   the best balance of performance, scalability, and simplicity
# In the worst case, we will have a lock for each parking spot of a level

# Benefits: (The hybrid approach is the best balance of performance, scalability, and simplicity)
#   - Locks are scoped within each floor, not globally.
#   - Locks are created lazily (on demand) — only when a spot is accessed.
#   - Each LockManager handles its own subset, reducing lock contention and lookup time.
#   - Easier to shard, monitor, and replace (e.g., per-floor distributed lock service).


# For distributed lock service, we can use Redis or ZooKeeper or Consul or etcd or any other distributed lock service instead of theading.lock


class LockManager:
    def __init__(self):
        self.spot_locks: dict[int, Lock] = defaultdict(Lock)  # spot number to lock
        self._manager_lock = Lock()  # To prevent race conditions between multiple threads trying to access the lock manager

    def get_lock(self, spot_id: int) -> Lock:
        with self._manager_lock:
            if spot_id not in self.spot_locks:
                self.spot_locks[spot_id] = Lock()
            return self.spot_locks[spot_id]

    @contextmanager  # (No need to manually handle __enter__ and __exit__ methods when using with 'with' keyword, context manager will handle it automatically)
    def acquire(self, spot_id: int) -> Generator[None, None, None]:
        lock = self.get_lock(spot_id)
        lock.acquire()
        try:
            yield  # Yielding None because we don't need to return anything from the context manager,
            # temporarily hand control back to the `with` block (i.e the code block that is using the context manager)
            # We will use as with lock_manager.acquire(spot_id) not as with lock_manager.get_lock(spot_id) as Lock
            # If We wanted to do with lock_manager.get_lock(spot_id) as Lock, we have to yield the lock i.e on line 51 instead of yield , we will have to do yield lock

        finally:
            lock.release()
            # we are not returning anything from the context manager, so we are returning None (3rd argument of the Generator)

    # Why Generator [None, None, None]?
    # Because we don't need to return anything from the context manager,
    # and we don't need to pass any arguments to the context manager.
    # So, the context manager will return None.
    # And the code block that is using the context manager will receive None.
    # And the code block that is using the context manager will receive None.

    # Generator [YieldType, ReturnType, ReturnType]
    # YieldType is the type of the value that is yielded by the context manager
    # ReturnType is the type of the value that is returned by the context manager
    # ReturnType is the type of the value that is returned by the context manager

    # Sample for custom context manager
    # def countdown(start: int) -> Generator[int, str, str]:
    # print(f"Starting countdown from {start}")
    # try:
    #     msg = yield start
    #     print(f"Received message from caller: {msg}")
    #     yield start - 1
    # finally:
    #     print("Countdown complete.")
    # return "Done!"

    # Try to call this code, you will see the output
    # gen = countdown(5)
    # print(next(gen))  # yields 5
    # print(gen.send("Keep going"))  # yields 4
    # try:
    #     next(gen)
    # except StopIteration as e:
    #     print(e.value)
