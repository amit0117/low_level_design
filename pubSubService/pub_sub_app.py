from app.factories.pub_sub_factory import PubSubFactory, BrokerConfigFactory
from app.models.topic import Topic
from app.models.subscriber import MessageSubscriber
from app.repositories.topic_repository import get_topic_repository
from app.models.enums import BrokerType, MessagePersistenceStrategy


class PubSubApp:
    def __init__(self, broker_name: str = "PubSubBroker", config_type: BrokerType = BrokerType.RABBITMQ):
        self.broker = self._create_broker(config_type, broker_name)
        self.topic_repo = get_topic_repository()

    def _create_broker(self, config_type: BrokerType, name: str):
        if config_type == BrokerType.KAFKA:
            return BrokerConfigFactory.create_kafka_like_broker(name)
        elif config_type == BrokerType.SQS:
            return BrokerConfigFactory.create_sqs_like_broker(name)
        else:
            return BrokerConfigFactory.create_rabbitmq_like_broker(name)

    def create_topic(self, topic_name: str, storage_type: MessagePersistenceStrategy = MessagePersistenceStrategy.IN_MEMORY):
        topic, queue = PubSubFactory.create_topic_with_queue(topic_name, storage_type.value)
        self.broker.add_topic(topic, queue)
        self.topic_repo.add_topic(topic)
        return topic

    def create_subscriber(self, name: str) -> MessageSubscriber:
        return PubSubFactory.create_subscriber(name)

    def create_publisher(self):
        return PubSubFactory.create_publisher(self.broker)

    def subscribe(self, topic_name: str, subscriber: MessageSubscriber) -> bool:
        topic = self.topic_repo.get_topic_by_name(topic_name)
        if topic:
            subscriber.subscribe_to_topic(topic)
            return True
        return False

    def unsubscribe(self, topic_name: str, subscriber: MessageSubscriber) -> bool:
        topic = self.topic_repo.get_topic_by_name(topic_name)
        if topic:
            subscriber.unsubscribe_from_topic(topic)
            return True
        return False

    def publish(self, topic_name: str, payload: str) -> bool:
        topic = self.topic_repo.get_topic_by_name(topic_name)
        if not topic:
            return False
        message = PubSubFactory.create_message(topic, payload)
        return self.broker.publish(message)

    def start(self):
        self.broker.start_consumption()

    def stop(self):
        self.broker.stop_consumption()

    def get_topic(self, topic_name: str) -> Topic | None:
        return self.topic_repo.get_topic_by_name(topic_name)

    def pull_message(self, topic_name: str):
        """Pull a message from the specified topic (for pull-based consumption)."""
        topic = self.get_topic(topic_name)
        if topic:
            try:
                return self.broker.pull_message(topic)
            except ValueError as e:
                return None
        return None
