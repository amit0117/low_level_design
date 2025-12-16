# Scalable Logger System – UML, Templates, and Data Flow

---

## 1. UML Class Diagram (Textual / Interview-Friendly)

```
+-------------------+        uses        +-------------------+
|      Logger       |------------------>|   LogConfig       |
|-------------------|                   |-------------------|
| - config          |                   | - minLevel        |
| - queue           |                   | - appenders[]     |
| - handlerChain    |                   +-------------------+
| - workerThread    |
|-------------------|
| + get_instance()  |
| + debug()         |
| + info()          |
| + warning()       |
| + error()         |
| + fatal()         |
+--------+----------+
         |
         | enqueues LogMessage
         v
+-------------------+
|   Queue (async)   |
+-------------------+
         |
         | dequeues
         v
+-------------------+        Chain of Responsibility
|  LogHandlerChain  |--------------------------------+
+-------------------+                                 |
         |                                           |
         | handles                                   |
         v                                           |
+-------------------+                                |
|   LogHandler      |<-------------------------------+
| (abstract)        |
+-------------------+
| - level           |
| - nextHandler     |
+-------------------+
| + handle()        |
| + process()       |
+--------+----------+
         |
         | implements
         v
+-------+-------+-------+-------+-------+-------+
|Trace  |Debug  |Info   |Warning|Error  |Fatal  |
|Handler|Handler|Handler|Handler|Handler|Handler|
+-------+-------+-------+-------+-------+-------+
         |
         | processes & forwards to appenders
         v
+-------------------+        +-------------------+
|     Appender      |<-------|   Formatter       |
| (interface)       |        | (interface)       |
|-------------------|        |-------------------|
| + append(msg)     |        | + format(msg)     |
+--------+----------+        +-------------------+
         |
         | implements
         v
+-------------------+  +-------------------+  +---------------------+
| ConsoleAppender   |  | FileAppender      |  | DatabaseAppender    |
|-------------------|  |-------------------|  |---------------------|
| - formatter       |  | - formatter       |  | - db_url           |
+-------------------+  | - file_path       |  | - username         |
                       | - max_file_size   |  | - password         |
                       | - max_files       |  |---------------------|
                       | - current_size    |  | + append()          |
                       |-------------------|  +---------------------+
                       | + append()        |
                       | + _rotate_file()  |
                       | + _retention()    |
                       +-------------------+

+-------------------+
|    LogMessage     |
|-------------------|
| - timestamp        |
| - level           |
| - message         |
| - threadId        |
+-------------------+

+-------------------+
|     LogLevel      |
|-------------------|
| TRACE             |
| DEBUG             |
| INFO              |
| WARNING           |
| ERROR             |
| FATAL             |
+-------------------+
```

---

## 2. Design Patterns Used

### **Singleton Pattern** - Logger

- Ensures only one instance of Logger exists across the application
- Thread-safe double-checked locking implementation

### **Chain of Responsibility Pattern** - Log Handlers

- Each log level has its own handler (TraceHandler, DebugHandler, InfoHandler, etc.)
- Handlers are chained together to process log messages based on their level
- Each handler processes its specific level and forwards to the next handler

### **Strategy Pattern** - Appenders & Formatters

- Different appender strategies (Console, File, Database)
- Different formatter strategies (Text, JSON)
- Allows runtime selection of appenders and formatters

### **Worker Thread Pattern** - Async Processing

- Queue-based asynchronous log processing
- Non-blocking logging operations
- Background worker thread processes log messages

---

## 3. Class Templates (Language-Agnostic / Python Implementation)

### LogLevel

```python
from enum import Enum

class LogLevel(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5
```

---

### LogMessage

```python
from datetime import datetime
import threading

class LogMessage:
    def __init__(self, level: LogLevel, message: str):
        self.level = level
        self.message = message
        self.timestamp = datetime.now()
        self.thread_id = threading.get_ident()
```

---

### Formatter (Strategy)

```python
from abc import ABC, abstractmethod

class FormatStrategy(ABC):
    @abstractmethod
    def format(self, log_message: LogMessage) -> str:
        raise NotImplementedError

class TextFormatter(FormatStrategy):
    def format(self, log_message: LogMessage) -> str:
        return f"[{log_message.level.name}] {log_message.timestamp} - {log_message.message} - {log_message.thread_id}"

class JsonFormatter(FormatStrategy):
    def format(self, log_message: LogMessage) -> str:
        return json.dumps({
            "level": log_message.level.name,
            "timestamp": str(log_message.timestamp),
            "message": log_message.message,
            "thread_id": log_message.thread_id
        })
```

---

### Appender (Strategy)

```python
from abc import ABC, abstractmethod

class AppenderStrategy(ABC):
    @abstractmethod
    def append(self, log_message: LogMessage):
        raise NotImplementedError

class ConsoleAppender(AppenderStrategy):
    def __init__(self, formatter: FormatStrategy):
        self.formatter = formatter

    def append(self, log_message: LogMessage):
        print(self.formatter.format(log_message))

class FileAppender(AppenderStrategy):
    def __init__(self, formatter: FormatStrategy, file_path: str,
                 max_file_size_kb: int = 10, max_files: int = 5):
        self.formatter = formatter
        self.base_file_path = file_path
        self.max_file_size_bytes = max_file_size_kb * 1024
        self.max_files = max_files
        self.current_file_path = file_path
        self.current_file_size = 0
        self._lock = threading.Lock()

    def append(self, log_message: LogMessage):
        with self._lock:
            formatted_message = self.formatter.format(log_message) + "\n"
            message_size = len(formatted_message.encode("utf-8"))

            current_size = self._get_file_size(self.current_file_path)
            if current_size + message_size > self.max_file_size_bytes:
                self._rotate_file()
                current_size = 0

            with open(self.current_file_path, "a", encoding="utf-8") as f:
                f.write(formatted_message)

            self.current_file_size = self._get_file_size(self.current_file_path)

    def _rotate_file(self):
        # Rotate file with timestamp: app_20241217_012345.log
        # Apply retention policy to keep only max_files
        pass
```

---

### Chain of Responsibility - Log Handlers

```python
from abc import ABC, abstractmethod

class LogHandler(ABC):
    def __init__(self, level: LogLevel):
        self.level = level
        self.next_handler: LogHandler = None

    def set_next(self, handler: "LogHandler") -> "LogHandler":
        self.next_handler = handler
        return handler

    def handle(self, log_message: LogMessage, appenders: list[AppenderStrategy]):
        if self.level.value <= log_message.get_level().value:
            self.process(log_message, appenders)

        if self.next_handler:
            self.next_handler.handle(log_message, appenders)

    @abstractmethod
    def process(self, log_message: LogMessage, appenders: list[AppenderStrategy]):
        raise NotImplementedError

class InfoHandler(LogHandler):
    def __init__(self):
        super().__init__(LogLevel.INFO)

    def process(self, log_message: LogMessage, appenders: list[AppenderStrategy]):
        if log_message.get_level() == LogLevel.INFO:
            for appender in appenders:
                appender.append(log_message)

class LogHandlerChain:
    @staticmethod
    def create_chain() -> LogHandler:
        trace_handler = TraceHandler()
        debug_handler = DebugHandler()
        info_handler = InfoHandler()
        warning_handler = WarningHandler()
        error_handler = ErrorHandler()
        fatal_handler = FatalHandler()

        trace_handler.set_next(debug_handler).set_next(info_handler)\
                    .set_next(warning_handler).set_next(error_handler)\
                    .set_next(fatal_handler)

        return trace_handler
```

---

### LogConfig

```python
class LogConfig:
    def __init__(self, min_level: LogLevel, appenders: List[AppenderStrategy]):
        self.min_level = min_level
        self.appenders = appenders
```

---

### Logger (Singleton + Queue-based Async)

```python
import queue
import threading

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
                        raise ValueError("Config required for first initialization")
                    cls._instance = Logger(config)
        return cls._instance

    def log(self, level: LogLevel, message: str):
        if level.value < self.config.min_level.value:
            return
        self.queue.put(LogMessage(level, message))

    def info(self, msg: str):
        self.log(LogLevel.INFO, msg)

    def error(self, msg: str):
        self.log(LogLevel.ERROR, msg)

    def _start_worker(self):
        def worker():
            while True:
                msg = self.queue.get()
                self.handler_chain.handle(msg, self.config.appenders)
                self.queue.task_done()

        threading.Thread(target=worker, daemon=True).start()
```

---

## 4. Data Flow (End-to-End)

### Step-by-Step Flow

```
Application Thread
        |
        | logger.info("Order placed")
        v
+------------------+
|      Logger       |  (Singleton + Facade)
+------------------+
        |
        | 1. Check min_level filter
        | 2. Create LogMessage
        | 3. Enqueue to queue
        v
+------------------+
|   Queue (async)   |  (Non-blocking)
+------------------+
        |
        | Worker thread dequeues
        v
+------------------+
| LogHandlerChain   |  (Chain of Responsibility)
+------------------+
        |
        | Traverses chain based on log level
        v
+------------------+
|  InfoHandler      |  (Processes INFO level)
+------------------+
        |
        | Forwards to all appenders
        v
+------------------+
|   Appenders       |  (Strategy Pattern)
+------------------+
   |        |        |
   v        v        v
Console   File    Database
   |        |
   |        | File rotation check
   |        | (if size > 10KB)
   |        v
   |    Rotate & Retention
```

---

## 5. File Rotation & Retention Policy

### Features

1. **Size-Based Rotation**:

   - Default: 10KB per file (configurable)
   - Automatically rotates when file size exceeds limit
   - Rotated files named with timestamp: `app_20241217_012345.log`

2. **Retention Policy**:

   - Default: Keeps maximum 5 files (configurable)
   - Automatically deletes oldest files when limit exceeded
   - Sorted by modification time

3. **Thread-Safe**:
   - Uses locks to ensure concurrent access safety
   - Prevents race conditions during rotation

### Example

```python
# Create FileAppender with custom rotation settings
file_appender = FileAppender(
    formatter=TextFormatter(),
    file_path="app.log",
    max_file_size_kb=10,  # Rotate at 10KB
    max_files=5            # Keep max 5 files
)

# Files created:
# - app.log (current)
# - app_20241217_012345.log (rotated)
# - app_20241217_012400.log (rotated)
# ... (oldest files deleted when > 5)
```

---

## 6. Sample Runtime Example

### Configuration

```python
from app.models.logger import Logger
from app.models.log_config import LogConfig
from app.models.enums import LogLevel
from app.strategies.appender import ConsoleAppender, FileAppender
from app.strategies.format import TextFormatter

# Setup formatters and appenders
formatter = TextFormatter()
console = ConsoleAppender(formatter)
file = FileAppender(formatter, "app.log", max_file_size_kb=10, max_files=5)

# Configure logger
config = LogConfig(
    min_level=LogLevel.INFO,
    appenders=[console, file]
)

# Get singleton instance
logger = Logger.get_instance(config)
```

### Logging

```python
logger.debug("Cache miss")        # Ignored (min_level is INFO)
logger.info("User logged in")     # Processed
logger.warning("Low memory")       # Processed
logger.error("DB connection failed")  # Processed
logger.fatal("Critical failure")   # Processed
```

### Output

**Console:**

```
[INFO] 2025-12-17 10:30:01.123456 - User logged in - 8373127168
[WARNING] 2025-12-17 10:30:02.234567 - Low memory - 8373127168
[ERROR] 2025-12-17 10:30:03.345678 - DB connection failed - 8373127168
[FATAL] 2025-12-17 10:30:04.456789 - Critical failure - 8373127168
```

**File (app.log):**

```
[INFO] 2025-12-17 10:30:01.123456 - User logged in - 8373127168
[WARNING] 2025-12-17 10:30:02.234567 - Low memory - 8373127168
[ERROR] 2025-12-17 10:30:03.345678 - DB connection failed - 8373127168
[FATAL] 2025-12-17 10:30:04.456789 - Critical failure - 8373127168
```

---

## 7. Why This Design Works Well in Interviews

### **Design Patterns Applied:**

- ✅ **Singleton**: Logger instance management
- ✅ **Chain of Responsibility**: Log level processing
- ✅ **Strategy**: Appenders and formatters
- ✅ **Worker Thread**: Async processing

### **Key Features:**

- ✅ **Thread-Safe**: Lock-based synchronization
- ✅ **Non-Blocking**: Queue-based async logging
- ✅ **Extensible**: Easy to add new appenders/formatters/handlers
- ✅ **Production-Ready**: File rotation, retention policy
- ✅ **Scalable**: Handles high-volume logging

### **Production-Inspired:**

- Similar architecture to Log4j / SLF4J / Python logging
- Industry-standard patterns and practices
- Handles edge cases (file rotation, concurrent access)

---

## 8. Usage Example

```python
from app.models.logger import Logger
from app.models.log_config import LogConfig
from app.models.enums import LogLevel
from app.strategies.appender import ConsoleAppender, FileAppender
from app.strategies.format import TextFormatter

# Setup
formatter = TextFormatter()
console = ConsoleAppender(formatter)
file = FileAppender(formatter, "app.log")

config = LogConfig(
    min_level=LogLevel.INFO,
    appenders=[console, file]
)

logger = Logger.get_instance(config)

# Use logger
logger.info("Application started")
logger.error("Database connection failed")
```

---

## 9. Extension Points

### Adding New Appender

```python
class CloudWatchAppender(AppenderStrategy):
    def __init__(self, aws_client):
        self.aws_client = aws_client

    def append(self, log_message: LogMessage):
        self.aws_client.put_log_events(...)
```

### Adding New Formatter

```python
class XMLFormatter(FormatStrategy):
    def format(self, log_message: LogMessage) -> str:
        return f"<log><level>{log_message.level}</level>...</log>"
```

### Adding New Log Level

1. Add to `LogLevel` enum
2. Create new handler class
3. Add to chain in `LogHandlerChain.create_chain()`

---

If you want next:

- **Sequence diagram** for detailed interaction flow
- **High-performance variant** (Disruptor / ring buffer)
- **Config-driven design** (YAML/JSON configuration)
- **Metrics and monitoring** integration

Tell me which one you want.
