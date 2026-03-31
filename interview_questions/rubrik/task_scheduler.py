# Design a system where:
#   Tasks are submitted with a scheduled execution time (timestamp / delay)
#   Multiple worker threads execute tasks at the correct time
#   The system is thread-safe
#   Tasks should not run before their scheduled time
#   Efficient handling of
#   i. many tasks
#   ii. concurrent producers (adding tasks)
#   iii. concurrent consumers (executing tasks)
#   iv. Typical Api:
#   v. schedule(task: Callable, run_at: timestamp)
#
# Key Requirements
#   Time-based ordering
#   Earliest task executes first ( Use min-heap / priority queue for this)
#
# Concurrency
#   Multiple threads adding tasks
#   Worker thread(s) executing tasks
#
# Efficient waiting
#   Don’t busy-wait (Use Condition Variable wait-notify for this)
#
# Correctness
#   If a new earlier task arrives → wake up workers, So for this as soon as we will schedule any task we will nofity threads which are blocking on this
#   For this we will use Condition Variable, and we can do both notify and notify_all, but in this case notify_all is not benificial
#   and might cause 'Thundering herd' problem

# 1.Why notify() (1 thread) vs notify_all()?
#   What happens with notify_all()
#   All waiting workers wake up.They race for the same lock. Only one thread actually gets the task.
#   Others, reacquire lock, re-check condition & go back to sleep. This creates thundering herd problem
#   Excess context switching & CPU waste (lock contention)
# Why notify(i.e n=1) is enough?
#   At any moment, Only 1 task (top of heap) is eligible to run. So, We only need 1 worker to wake up and process it
#   Waking more threads gives no throughput benefit, only overhead.


# Follow ups
# 1. Multiple workers-> for producers and consumers
# 2. Recurring tasks?
#    After execution → reschedule
#    For this when we will pick the task from the queue/heap then we will check if the task is Recurring
#    then we will again schedule this task with the delay with respect to current_time / previous_scheduled time (Depends on the requirement). We will go for now() + delay
#    Also confirm, if we need to recurre the cancel task or not (For now, we will assume that cancelled task will not recur)

# 3. Cancel task?
#    Use task_id + lazy deletion (mark invalid), Because we are using heap for the smallest delay time task, and heap doesn't allow ot delete any element randomly
#    So, we will have a dict of task_id with status which will store if the task_id is Cancelled or not, By doing this
#    When we take any task from the heap and before we execute this task, we first check if this task has been cancelled or not and only execute if this task has not been cancelled

from threading import Thread,Condition
from typing import Callable
from heapq import heappush,heappop
import time
from uuid import uuid4
from enum import StrEnum,auto,Enum
import random
from datetime import datetime

class TaskType(StrEnum):
    NORMAL=auto()
    RECURRING=auto()

class TaskStatus(StrEnum):
    SCHEDULED=auto()
    CANCELLED=auto()
    COMPLETED=auto()

class RecurringType(Enum):
    seconds_in_day=24*60*60

    SECONDLY=2 # 2 Seconds for now
    MINUTELY= 1*60 # 1 minute for now
    DAILY=seconds_in_day
    WEEKLY=7*seconds_in_day
    MONTHLY=30*seconds_in_day
    YEARLY=365*seconds_in_day

    def __init__(self,seconds_in_day:int):
        self._delay=seconds_in_day

    @property
    def delay(self):
        return self._delay


class Task:
    def __init__(self,fn:Callable,delay:int,task_type:TaskType|None=None,recurring_type:RecurringType|None=None):
        self.task_id=str(uuid4())
        self.fn=fn
        self.delay=delay
        self.task_type=task_type
        self.recurring_type=recurring_type
        self.status=TaskStatus.SCHEDULED

    def update_status(self,updated_status:TaskStatus):
        self.status=updated_status

    def update_task_delay_time(self,updated_delay:int)->None:
        self.delay=updated_delay

    def make_task_recurring(self,recurring_type: RecurringType)->None:
        self.task_type=TaskType.RECURRING
        self.recurring_type=recurring_type

class TaskScheduler:
    def __init__(self,consumer_workers:int=1):
        # each entry will be a tuple (run_at,task_id,task) Add task_id for the tie breaker as Heap doesn't allow key parameter for custom comparator and relies on __lt__ implementation
        self.task_heap=[]
        self.cond_var=Condition()
        # will store the status of a task (i.e active or cancelled/removed)
        self.task_status:dict[str,TaskStatus]=dict()

        # Making these worker threads as daemon because we want to die those workers threads when main threads ends
        self.worker_threads=[Thread(target=self.consumer_worker,name=f"Consumer_Worker_thread_{i}",daemon=True) for i in range(consumer_workers)]

        # Starting all threads
        for thread in self.worker_threads:
            thread.start()

    def schedule(self,task:Task)->str:
        run_at=time.time() + task.delay
        curr_task_id=task.task_id

        with self.cond_var:
            heappush(self.task_heap,(run_at,curr_task_id,task))
            self.task_status[curr_task_id]=task.status
            # notify the waiting thread so that if this task is having the lowest time it could process first or else other thread waiting for this this condition shoudl wake up and re-evaluate
            # Commented why here notify() is more suitable than notify_all()
            # Also to optimize this we can only notify if the heap was empty or the run_at is the minimum (this avoids unnecessary wakeups)
            if len(self.task_heap)==1 or self.task_heap[0][0] == run_at:
               self.cond_var.notify()

        return curr_task_id

    def cancel_task(self,task_id:str):
        with self.cond_var:
            if self.task_status.get(task_id) == TaskStatus.SCHEDULED:
                # Mark this task as cancelled
                self.task_status[task_id]=TaskStatus.CANCELLED


    def consumer_worker(self):
        while True:
            with self.cond_var:

                # wait till heap is empty
                while not self.task_heap:
                    self.cond_var.wait()

                run_at,_,task=self.task_heap[0]
                now=time.time()

                if run_at-now>0:
                    self.cond_var.wait(run_at-now)
                    # Why continue? because we want to start the whole run_at and now check from start after left time
                    # we can use while condition here as well, but then we have to perform these run_at,task_id,task=self.task_heap[0]
                    # now=time.time() , Checks inside the while loop. And using continue will achieve the same
                    continue

                # if reach here then current time > run_at, remove from the heap
                heappop(self.task_heap)

            # process task outside of the lock
            self._execute_task(task)

    def _execute_task(self,task:Task)->None:
        # check if this is cancelled or not
        if self.task_status.get(task.task_id)==TaskStatus.CANCELLED:
            print(f"Task {task.task_id} had cancelled")
            self.task_status.pop(task.task_id)
            # cancelled task will not be processed and recurr
            return

        try:
            task.fn()
        finally:
            # updated status as COMPLETED
            task.update_status(TaskStatus.COMPLETED)
            # remove from the task_status and check if this is recurring (if recurring we will schedule after corresponding time)
            self.task_status.pop(task.task_id)
            self.recur_schedule(task)

    def recur_schedule(self,task:Task)->None:
        if task.task_type==TaskType.RECURRING:
            # change status as SCHEDULED
            task.update_status(TaskStatus.SCHEDULED)
            # Update the delay time for this task
            task.update_task_delay_time(task.recurring_type.delay)
            self.schedule(task)
            print(f"Task with task_id {task.task_id} re-scheduled successfyully")




if __name__=="__main__":
    scheduler=TaskScheduler(consumer_workers=3)

    # similar to datetime we can also use time.strptime and time_in_str.strftime(format)
    # %H -> Hour, %M -> Minutes , %S -> Seconds, so we can use ("%H-%M-%S")
    # %X -> Locale’s appropriate time representation Eg, 12:06:45
    # %p ->	Locale’s AM or PM
    # %I ->	Hour (12-hour clock) 01 to 12

    time_format="%Y-%m-%d %H:%M:%S"

    def sample_task(name:str)->None:
        print(f"{datetime.now().strftime(time_format)} -> Started Task: {name}")
        time.sleep(random.randint(1,3))
        print(f"{datetime.now().strftime(time_format)} -> Ended Task: {name}")


    def create_task(name:str,delay:int)->Task:
        return Task(lambda :sample_task(name),delay)

    total_task=10
    tasks=[create_task(f"Task_{i+1}",total_task-i) for i in range(total_task)]

    # update task 1 and 2 for recurring type
    for task in tasks[:2]:
        task.make_task_recurring(RecurringType.SECONDLY)


    # For Single Producer test
    # for task in tasks:
    #     scheduler.schedule(task)

    # test multiple producers , i will test with 2 thread
    # each thread will run 5 tasks
    def producer(start_idx:int):
        for i in range(5):
            scheduler.schedule(tasks[start_idx+i])


    producer_thread_count=2
    producer_threads=[]
    for i in range(producer_thread_count):
        start_idx=0 if i==0 else 5
        thread=Thread(target=producer,args=(start_idx,))
        thread.start()
        producer_threads.append(thread)

    # Recurring task (we will make task1 and task2 as recurring and then we will cancel those)
    # So wait for 10 seconds for task1 and task2 to get rescheduled
    time.sleep(30)


    #Cancel Task Test
    def cancel_tasks(task_ids:list[str])->None:
        for task_id in task_ids:
            scheduler.cancel_task(task_id)
    # we will cancel task 1 and 2
    cancel_task_thread=Thread(target=cancel_tasks,args=([t.task_id for t in tasks[:2]],))
    cancel_task_thread.start()
    cancel_task_thread.join()



    # wait the main thread for 20 Seconds for the consumer thread to drain the tasks
    time.sleep(60)
