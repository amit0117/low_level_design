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
        self.queue.put(LogMessage(level, message))

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
                msg = self.queue.get()
                self.handler_chain.handle(msg, self.config.appenders)
                self.queue.task_done()

        threading.Thread(target=worker, daemon=True).start()
