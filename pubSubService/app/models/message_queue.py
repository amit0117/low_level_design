from app.strategies.message_persistence_strategy import MessageQueueStrategy, inMemoryMessageQueueStrategy
from app.models.message import Message


class MessageQueue:
    def __init__(self, strategy: MessageQueueStrategy = inMemoryMessageQueueStrategy()):
        self.message_queue_strategy = strategy

    def set_message_queue_strategy(self, strategy: MessageQueueStrategy) -> None:
        self.message_queue_strategy = strategy

    def add_message_to_queue(self, message: Message) -> None:
        self.message_queue_strategy.enqueue(message)

    def get_message_from_queue(self) -> Message:
        return self.message_queue_strategy.dequeue()
