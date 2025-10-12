from abc import ABC, abstractmethod


class BankIntegrationFactory(ABC):
    @abstractmethod
    def create_connector(self):
        raise NotImplementedError("create_connector method must be implemented")

    @abstractmethod
    def create_auth_handler(self):
        raise NotImplementedError("create_auth_handler method must be implemented")

    @abstractmethod
    def create_formatter(self):
        raise NotImplementedError("create_formatter method must be implemented")

    @abstractmethod
    def create_notifier(self):
        raise NotImplementedError("create_notifier method must be implemented")
