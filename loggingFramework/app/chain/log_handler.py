from abc import ABC, abstractmethod
from app.models.log_message import LogMessage
from app.models.enums import LogLevel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.strategies.appender import AppenderStrategy


class LogHandler(ABC):
    def __init__(self, level: LogLevel):
        self.level = level
        self.next_handler: LogHandler = None

    def set_next(self, handler: "LogHandler") -> "LogHandler":
        self.next_handler = handler
        return handler

    def handle(self, log_message: LogMessage, appenders: list["AppenderStrategy"]):
        if self.level.value <= log_message.get_level().value:
            self.process(log_message, appenders)

        if self.next_handler:
            self.next_handler.handle(log_message, appenders)

    @abstractmethod
    def process(self, log_message: LogMessage, appenders: list["AppenderStrategy"]):
        raise NotImplementedError("Subclasses must implement this method")


class TraceHandler(LogHandler):
    def __init__(self):
        super().__init__(LogLevel.TRACE)

    def process(self, log_message: LogMessage, appenders: list["AppenderStrategy"]):
        if log_message.get_level() == LogLevel.TRACE:
            for appender in appenders:
                appender.append(log_message)


class DebugHandler(LogHandler):
    def __init__(self):
        super().__init__(LogLevel.DEBUG)

    def process(self, log_message: LogMessage, appenders: list["AppenderStrategy"]):
        if log_message.get_level() == LogLevel.DEBUG:
            for appender in appenders:
                appender.append(log_message)


class InfoHandler(LogHandler):
    def __init__(self):
        super().__init__(LogLevel.INFO)

    def process(self, log_message: LogMessage, appenders: list["AppenderStrategy"]):
        if log_message.get_level() == LogLevel.INFO:
            for appender in appenders:
                appender.append(log_message)


class WarningHandler(LogHandler):
    def __init__(self):
        super().__init__(LogLevel.WARNING)

    def process(self, log_message: LogMessage, appenders: list["AppenderStrategy"]):
        if log_message.get_level() == LogLevel.WARNING:
            for appender in appenders:
                appender.append(log_message)


class ErrorHandler(LogHandler):
    def __init__(self):
        super().__init__(LogLevel.ERROR)

    def process(self, log_message: LogMessage, appenders: list["AppenderStrategy"]):
        if log_message.get_level() == LogLevel.ERROR:
            for appender in appenders:
                appender.append(log_message)


class FatalHandler(LogHandler):
    def __init__(self):
        super().__init__(LogLevel.FATAL)

    def process(self, log_message: LogMessage, appenders: list["AppenderStrategy"]):
        if log_message.get_level() == LogLevel.FATAL:
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

        trace_handler.set_next(debug_handler).set_next(info_handler).set_next(warning_handler).set_next(error_handler).set_next(fatal_handler)

        return trace_handler
