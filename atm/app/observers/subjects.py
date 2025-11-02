from app.observers.base_observer import BaseObserver


class BaseSubject:
    def __init__(self):
        self.observers: list[BaseObserver] = []

    def add_observer(self, observer: BaseObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: BaseObserver) -> None:
        self.observers.remove(observer)

    def notify_observers(self, message: str) -> None:
        for observer in self.observers:
            observer.update(message)


# We will use the base subject to create the subjects for the Transaction, ATMLowCashAlert, etc.
