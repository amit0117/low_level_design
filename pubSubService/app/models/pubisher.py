from app.models.broker import Broker
from app.models.message import Message


class Publisher:
    def __init__(self, broker: Broker):
        self.broker = broker

    def publish(self, message: Message) -> bool:
        return self.broker.publish(message)

    def set_broker(self, broker: Broker) -> None:
        self.broker = broker

    def get_broker(self) -> Broker:
        return self.broker
