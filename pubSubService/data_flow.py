"""
Mermaid Diagrams for Pub-Sub Service - Low Level Design
"""

DATA_FLOW_DIAGRAM = """
```mermaid
graph TD
    Publisher[Publisher] -->|publishes| Message[Message]
    Message -->|sent to| Broker{Broker}
    Broker -->|RabbitMQ| RabbitMQ[RabbitMQ Broker]
    Broker -->|Kafka| Kafka[Kafka Broker]

    Message -->|belongs to| Topic[Topic]
    Topic -->|stored in| TopicRepository[TopicRepository]
    Broker -->|manages| MessageQueue[MessageQueue]
    MessageQueue -->|stored in| MQRepository[MessageQueueRepository]

    Broker -->|routes via| RoutingStrategy{Message Routing Strategy}
    RoutingStrategy -->|broadcast| Broadcast[BroadCastMessageRoutingStrategy]
    RoutingStrategy -->|round robin| RoundRobin[RoundRobinMessageRoutingStrategy]

    Broker -->|delivers via| DeliveryStrategy{Message Delivery Strategy}
    DeliveryStrategy -->|at least once| AtLeastOnce[AtLeastOnce]
    DeliveryStrategy -->|at most once| AtMostOnce[AtMostOnce]

    Broker -->|consumed via| ConsumptionStrategy{Message Consumption Strategy}
    ConsumptionStrategy -->|push| Push[PushConsumptionStrategy]
    ConsumptionStrategy -->|pull| Pull[PullConsumptionStrategy]

    MessageSubscriber[MessageSubscriber] -->|subscribes to| Topic
    MessageSubscriber -->|stored in| SubscriberRepository[SubscriberRepository]
    Broker -->|delivers to| MessageSubscriber

    Message -->|retry via| RetryStrategy{Message Retry Strategy}
    RetryStrategy -->|exponential| Exponential[ExponentialBackoffRetry]
    RetryStrategy -->|fixed| Fixed[FixedIntervalRetry]
    RetryStrategy -->|jitter| Jitter[JitterRetry]
    RetryStrategy -->|none| NoRetry[NoRetry]

    Message -->|persisted via| Persistence[MessagePersistenceStrategy]

    Message -->|observed by| MessageObserver[MessageObserver]
    MessageObserver -->|notifies| MessageSubscriber
```
"""

USER_FLOW_DIAGRAM = """
```mermaid
sequenceDiagram
    actor Publisher
    actor Subscriber
    participant Broker
    participant Topic
    participant Queue as MessageQueue
    participant Router as RoutingStrategy
    participant Delivery as DeliveryStrategy
    participant RetryStrategy

    Publisher->>Topic: Create topic
    Subscriber->>Topic: Subscribe to topic

    Publisher->>Broker: Publish message to topic
    Broker->>Queue: Enqueue message
    Broker->>Router: Route message

    alt Broadcast
        Router->>Router: Send to ALL subscribers
    else Round Robin
        Router->>Router: Send to NEXT subscriber
    end

    Broker->>Delivery: Deliver message
    alt Push Strategy
        Delivery->>Subscriber: Push message to subscriber
    else Pull Strategy
        Subscriber->>Delivery: Pull message from queue
    end

    alt Processing successful
        Subscriber->>Broker: Acknowledge message
        Broker->>Queue: Remove message

        alt Persistent mode
            Broker->>Broker: Persist to storage
        end
    else Processing failed
        Subscriber-->>Broker: Negative acknowledgment

        Broker->>RetryStrategy: Retry delivery
        alt Exponential Backoff
            RetryStrategy->>RetryStrategy: Wait 1s, 2s, 4s, 8s...
        else Fixed Interval
            RetryStrategy->>RetryStrategy: Wait fixed duration
        else Jitter
            RetryStrategy->>RetryStrategy: Wait random duration
        end

        RetryStrategy->>Delivery: Redeliver message
        Delivery->>Subscriber: Retry message delivery
        Subscriber->>Broker: Acknowledge on success
    end
```
"""

if __name__ == "__main__":
    print("=" * 60)
    print("DATA FLOW DIAGRAM")
    print("=" * 60)
    print(DATA_FLOW_DIAGRAM)
    print("=" * 60)
    print("USER FLOW DIAGRAM")
    print("=" * 60)
    print(USER_FLOW_DIAGRAM)
