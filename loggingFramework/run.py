from app.models.logger import Logger
from app.models.log_config import LogConfig
from app.models.enums import LogLevel
from app.strategies.appender import ConsoleAppender, FileAppender
from app.strategies.format import TextFormatter
import time


def main():
    formatter = TextFormatter()
    console = ConsoleAppender(formatter)
    file = FileAppender(formatter, "app.log", max_file_size_kb=10, max_files=5)

    config = LogConfig(min_level=LogLevel.INFO, appenders=[console, file])

    logger = Logger.get_instance(config)

    print("📝 Logging Framework Demo")
    print("=" * 50)

    logger.info("Application started")
    logger.debug("This is a debug message (should not appear as min_level is INFO)")
    logger.warning("Warning: Low memory detected")
    logger.error("Database connection failed")
    logger.fatal("Critical system failure")

    print("\n🔄 Testing file rotation (generating logs to exceed 10KB limit)...")
    large_message = "X" * 500
    for i in range(30):
        logger.info(f"Log message #{i}: {large_message}")

    time.sleep(0.2)
    print("\n✅ Demo completed! Check 'app.log' and rotated log files for logs.")


if __name__ == "__main__":
    main()
