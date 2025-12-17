import queue
import threading
from app.models.log_config import LogConfig
from app.models.log_message import LogMessage
from app.models.enums import LogLevel
from app.chain.log_handler import LogHandlerChain


class Logger:
    _instance = None
    _lock = threading.Lock()

    def __init__(self, config: LogConfig):
        self.config = config
        self.queue = queue.Queue()
        self.handler_chain = LogHandlerChain.create_chain()
        self._start_worker()

    @classmethod
    def get_instance(cls, config: LogConfig = None):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    if config is None:
                        raise ValueError("Config is required for first initialization")
                    cls._instance = Logger(config)
        return cls._instance

    def log(self, level: LogLevel, message: str):
        if level.value < self.config.min_level.value:
            return
        self.queue.put(LogMessage(level, message))  # This is used to add the log message to the queue and increament the counter of the queue

    def info(self, msg: str):
        self.log(LogLevel.INFO, msg)

    def debug(self, msg: str):
        self.log(LogLevel.DEBUG, msg)

    def warning(self, msg: str):
        self.log(LogLevel.WARNING, msg)

    def error(self, msg: str):
        self.log(LogLevel.ERROR, msg)

    def fatal(self, msg: str):
        self.log(LogLevel.FATAL, msg)

    def _start_worker(self):
        def worker():
            while True:
                # This uses mutex behind the scenes to ensure that only one thread can access the queue at a time
                # Since has one property bock with default value as True, it will block the thread till it is not empty
                msg = self.queue.get()  # Gets item, counter stays same

                self.handler_chain.handle(msg, self.config.appenders)

                self.queue.task_done()  # Marks task as done, decrements counter

        # Daemon thread to run in the background indefinitely as when the main thread exits, the daemon threads will also exit
        # without any guaranteed termination/cleanup of resources like database connections, file handles, etc.
        # Here it is ideal to use because for demo we want it to run indefinitely and at the same time we want to exit when main thread exits.
        threading.Thread(target=worker, daemon=True).start()


# We can also implement PUB/SUB pattern here
# Because there might be different consumers of the logs like sending to a database, sending to a file, sending to a console, sending to a webhook, or sending it to kafka, ETL pipeline, etc.



# How Queue works:
# queue.put(item) — increments an internal counter
# queue.get() — gets an item (doesn't decrement the counter)
# queue.task_done() — decrements the counter, indicating the task is done
# queue.join() — blocks until all tasks are done (counter reaches 0)