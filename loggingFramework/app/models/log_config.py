from app.models.enums import LogLevel
from app.strategies.appender import AppenderStrategy
from app.strategies.format import FormatStrategy
from typing import List


class LogConfig:
    def __init__(self, min_level: LogLevel, appenders: List[AppenderStrategy]):
        self.min_level = min_level
        self.appenders = appenders

    def get_min_level(self) -> LogLevel:
        return self.min_level

    def set_min_level(self, min_level: LogLevel):
        self.min_level = min_level

    def get_appenders(self) -> List[AppenderStrategy]:
        return self.appenders

    def set_appenders(self, appenders: List[AppenderStrategy]):
        self.appenders = appenders

    def add_appender(self, appender: AppenderStrategy):
        if appender not in self.appenders:
            self.appenders.append(appender)

    def remove_appender(self, appender: AppenderStrategy):
        if appender in self.appenders:
            self.appenders.remove(appender)
