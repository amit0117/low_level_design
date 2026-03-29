# Concurrent Producer Consumer Problem
import time
import random
from threading import Thread
from queue import Queue

work_queue = Queue(maxsize=5)


def producer():
    for i in range(0, 5):
        item = f"Data item -- {i}"
        work_queue.put(item)
        print(f"Producer added: {item} to the queue\n")
        time.sleep(random.random())


def consumer():
    while True:
        item = work_queue.get()
        work_queue.task_done()
        print(f"Consumer processed: {item}")
        time.sleep(random.random())


producer_thread = Thread(target=producer, name="Producer")
consumer_thread = Thread(
    target=consumer, name="Consumer", daemon=True
).start()  # because we are using while loop in the consumer, so even if all elements from the queue will popped out and there is no change to addition of any new element in the producer queue, but If we don't mark this consumer thread as daemon so the main thread will wait for the consumer thread to finish, but consumer thread will never finish. in this way the complete program will hang
producer_thread.start()
producer_thread.join()  # wait the main thread till this producer thread completed

# wait till the queue has no pending item to process
# we will use the .join of queue which will block the program till the all the items which was ever added in the queue, has proceessed completelty
work_queue.join()
