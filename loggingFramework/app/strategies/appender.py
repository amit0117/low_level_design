from abc import ABC, abstractmethod
from app.models.log_message import LogMessage
import threading
from app.strategies.format import FormatStrategy, TextFormatter, JsonFormatter

try:
    import psycopg2
except ImportError:
    psycopg2 = None


class AppenderStrategy(ABC):
    @abstractmethod
    def append(self, log_message: LogMessage):
        raise NotImplementedError("Subclasses must implement this method")


class ConsoleAppender(AppenderStrategy):
    def __init__(self, formatter: FormatStrategy = None):
        self.formatter = formatter if formatter else (TextFormatter())

    def append(self, log_message: LogMessage):
        print(self.formatter.format(log_message))


import os
import glob
from datetime import datetime
from pathlib import Path


class FileAppender(AppenderStrategy):
    def __init__(self, formatter: FormatStrategy, file_path: str, max_file_size_kb: int = 10, max_files: int = 5):
        self.formatter = formatter if formatter else TextFormatter()
        self.base_file_path = file_path
        self.max_file_size_bytes = max_file_size_kb * 1024
        self.max_files = max_files
        self.current_file_path = file_path
        self.current_file_size = self._get_file_size(file_path)
        self._lock = threading.Lock()

    def _get_file_size(self, file_path: str) -> int:
        if os.path.exists(file_path):
            return os.path.getsize(file_path)
        return 0

    def _rotate_file(self):
        base_path = Path(self.base_file_path)
        directory = base_path.parent
        base_name = base_path.stem
        extension = base_path.suffix

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rotated_file = directory / f"{base_name}_{timestamp}{extension}"

        if os.path.exists(self.current_file_path):
            os.rename(self.current_file_path, str(rotated_file))

        self.current_file_path = self.base_file_path
        self.current_file_size = 0

        self._apply_retention_policy(directory, base_name, extension)

    def _apply_retention_policy(self, directory: Path, base_name: str, extension: str):
        pattern = str(directory / f"{base_name}_*{extension}")
        log_files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)

        if len(log_files) > self.max_files:
            for old_file in log_files[self.max_files :]:
                try:
                    os.remove(old_file)
                except OSError:
                    pass

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


class DatabaseAppender(AppenderStrategy):
    def __init__(self, db_url: str, username: str, password: str):
        if psycopg2 is None:
            raise ImportError("psycopg2 is required for DatabaseAppender. Install it using: pip install psycopg2-binary")
        self.db_url = db_url
        self.username = username
        self.password = password

    def append(self, log_message: LogMessage):
        try:
            connection = psycopg2.connect(self.db_url, self.username, self.password)
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO logs (level, message, timestamp) VALUES (%s, %s, %s)",
                (log_message.get_level().name, log_message.get_message(), log_message.get_timestamp()),
            )
            connection.commit()
        except psycopg2.Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


# we can extend this to cloudwatch, kafka etc
