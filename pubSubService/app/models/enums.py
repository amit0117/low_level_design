from enum import Enum


class BrokerType(Enum):
    RABBITMQ = "rabbitmq"
    KAFKA = "kafka"
    SQS = "sqs"


class MessagePersistenceStrategy(Enum):
    IN_MEMORY = "in-memory"
    FILE = "file"
