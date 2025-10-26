# Pub-Sub Messaging System

A comprehensive Low-Level Design (LLD) implementation of a publish-subscribe messaging system using Python, demonstrating advanced object-oriented design principles, design patterns, and concurrent programming techniques.

## 🏗️ System Architecture

This pub-sub system implements a robust, scalable architecture using multiple design patterns and threading concepts:

### Core Design Patterns Used

1. **Strategy Pattern** - Implements pluggable algorithms for routing, consumption, delivery, persistence, and retry
2. **Observer Pattern** - Topics notify subscribers about new messages
3. **Factory Pattern** - Creates configured brokers and entities
4. **Singleton Pattern** - Ensures single instance of repositories
5. **Repository Pattern** - Manages topic and subscriber data access
6. **Template Method** - Base strategies define algorithm structure

### Key Components

```
app/
├── models/           # Core domain entities
│   ├── broker.py     # Central message broker
│   ├── topic.py      # Topic with observer capabilities
│   ├── subscriber.py # Message subscribers
│   ├── publisher.py  # Message publishers
│   └── message.py    # Message entities
├── strategies/       # Strategy pattern implementations
│   ├── message_routing_strategy.py      # Broadcast, RoundRobin
│   ├── message_consumption_strategy.py  # Push, Pull
│   ├── message_delivery_strategy.py     # AtMostOnce, AtLeastOnce
│   ├── message_persistence_strategy.py  # InMemory, File
│   └── message_retry_strategy.py        # FixedInterval, ExponentialBackoff, Jitter
├── factories/        # Factory pattern
│   └── pub_sub_factory.py # Entity creation with configurations
├── repositories/     # Repository pattern
│   └── topic_repository.py # Topic data management
└── observers/        # Observer pattern
    └── message_observer.py # Subject/Observer base classes
```

## 🔄 Data Flow Architecture

```
Publisher
   |
   v
+------------------+
|      Broker      |
|------------------|
| Topics Registry  |
| Routing Strategy |
| Delivery Strategy|
| Retry Policy     |
+------------------+
   |
   v
Queues (per Topic)
   |
   +--> In-Memory / Persistent / Hybrid
   |
   v
Subscribers
   |
   +--> Push / Pull Consumption
   |
   v
Acknowledgement (for At-Least-Once/Exactly-Once)
   |
   v
Retry / Dead-Letter Queue if needed
```

## 🚀 Features

### Message Routing Strategies

- **Broadcast Routing**: All subscribers receive every message (RabbitMQ-style)
- **Round-Robin Routing**: Messages distributed to subscribers in rotation (Kafka-style)

### Consumption Models

- **Push Model**: Broker actively pushes messages to subscribers
- **Pull Model**: Subscribers explicitly request messages from broker

### Delivery Guarantees

- **At-Most-Once**: Messages may be lost but never duplicated
- **At-Least-Once**: Messages guaranteed to be delivered, may be duplicated

### Persistence Strategies

- **In-Memory**: Fast, volatile storage for development
- **File-Based**: Persistent storage for production scenarios

### Retry Strategies

- **Fixed Interval**: Retry with constant delay
- **Exponential Backoff**: Increasing delays between retries
- **Jitter**: Randomized delays to prevent thundering herd

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- No external dependencies required (pure Python implementation)

### Running the System

1. **Main Demo** (comprehensive demonstration):

```bash
cd low_level_design/pubSubService
python3 demo.py
```

This demo showcases:

- All routing strategies (Broadcast, Round-Robin)
- Both consumption models (Push, Pull)
- Different delivery guarantees (At-Most-Once, At-Least-Once)
- File-based persistence with retry mechanisms
- Dynamic subscription management
- Concurrent publishing with thread safety
- Graceful system shutdown

## 📊 System Behavior

### Message Flow

1. **Publisher Creation**: Publishers created through factory with broker reference
2. **Message Publishing**: Publisher sends message to broker with topic
3. **Topic Resolution**: Broker resolves topic and adds message to topic's queue
4. **Routing Decision**: Routing strategy determines target subscribers
5. **Delivery Execution**: Delivery strategy handles message delivery with retry logic
6. **Consumption**: Subscribers receive messages based on consumption model
7. **Acknowledgement**: Subscribers acknowledge receipt (for guaranteed delivery)

### Threading & Concurrency

- **Thread-Safe Operations**: All broker operations use proper locking
- **Producer-Consumer**: Publishers produce, broker routes, subscribers consume
- **Graceful Shutdown**: Clean termination of all background threads
- **Concurrent Publishing**: Multiple publishers can publish simultaneously

## 🎯 Design Principles Applied

### SOLID Principles

- **Single Responsibility**: Each class has one clear purpose (broker handles routing, strategies handle algorithms)
- **Open/Closed**: Easy to add new strategies without modifying existing code
- **Liskov Substitution**: All strategy implementations are interchangeable
- **Interface Segregation**: Clean, focused strategy interfaces
- **Dependency Inversion**: High-level modules depend on strategy abstractions

### Additional Principles

- **DRY (Don't Repeat Yourself)**: Reusable strategy and factory components
- **KISS (Keep It Simple, Stupid)**: Clear, understandable architecture
- **YAGNI (You Aren't Gonna Need It)**: Only implemented required messaging features

## 🔧 Configuration

### Broker Types

```python
# RabbitMQ-style (Push + Broadcast + At-Least-Once)
app = PubSubApp("MyApp", BrokerType.RABBITMQ)

# Kafka-style (Pull + Round-Robin + At-Least-Once)
app = PubSubApp("MyApp", BrokerType.KAFKA)

# SQS-style (Pull + Round-Robin + At-Least-Once with Jitter)
app = PubSubApp("MyApp", BrokerType.SQS)
```

### Strategy Configuration

```python
# Custom broker with specific strategies
broker = PubSubFactory.create_broker(
    name="CustomBroker",
    consumption_model="pull",
    delivery_guarantee="at-least-once"
)
```

## 📈 Performance Characteristics

### Routing Strategies

- **Broadcast**: O(n) where n = number of subscribers
- **Round-Robin**: O(1) per message with O(n) subscriber lookup

### Consumption Models

- **Push**: Lower latency, higher resource usage
- **Pull**: Higher latency, better resource control

### Delivery Guarantees

- **At-Most-Once**: Fastest, may lose messages
- **At-Least-Once**: Reliable, may duplicate messages

## 🧪 Demo Scenarios

The system includes 7 comprehensive demo scenarios:

1. **RabbitMQ Broadcast**: Push model with broadcast routing
2. **Kafka Round-Robin**: Pull model with load balancing
3. **File Persistence**: At-least-once delivery with file storage
4. **Subscription Management**: Dynamic subscribe/unsubscribe
5. **Multiple Topics**: Different services on different topics
6. **Concurrent Publishing**: Multiple publishers with thread safety
7. **Thread Safety**: Concurrent operations verification

## 🔍 Implementation Details

### Strategy Pattern Usage

```python
# Routing strategies
routing_strategy = BroadCastMessageRoutingStrategy()    # All subscribers
routing_strategy = RoundRobinMessageRoutingStrategy()   # Load balancing

# Consumption strategies
consumption_strategy = PushConsumptionStrategy(broker)  # Active pushing
consumption_strategy = PullConsumptionStrategy(broker)  # On-demand pulling

# Delivery strategies
delivery_strategy = AtMostOnce(retry_strategy)          # Fire and forget
delivery_strategy = AtLeastOnce(retry_strategy)         # Guaranteed delivery
```

### Observer Pattern Implementation

```python
# Topics are subjects, subscribers are observers
topic = Topic("Orders")
subscriber = MessageSubscriber("OrderService")

# Subscription creates observer relationship
topic.subscribe(subscriber)

# Publishing notifies all observers
topic.notify(message)
```

### Factory Pattern Benefits

```python
# Pre-configured brokers for common use cases
rabbitmq_broker = BrokerConfigFactory.create_rabbitmq_like_broker()
kafka_broker = BrokerConfigFactory.create_kafka_like_broker()
sqs_broker = BrokerConfigFactory.create_sqs_like_broker()
```

## 🚀 Future Enhancements

### Potential Improvements

- **Message Filtering**: Content-based routing with wildcards
- **Message Ordering**: Guaranteed order within topics/partitions
- **Clustering**: Distributed broker architecture
- **Message TTL**: Time-to-live for message expiration
- **Priority Queues**: High-priority message handling
- **Metrics & Monitoring**: Performance monitoring and alerting

### Extensibility Points

- **New Routing Strategies**: Implement `MessageRoutingStrategy`
- **New Consumption Models**: Extend `MessageConsumptionStrategy`
- **New Delivery Guarantees**: Implement `MessageDeliveryStrategy`
- **New Persistence Backends**: Extend `MessageQueueStrategy`

## 📚 Learning Outcomes

This project demonstrates:

1. **Advanced Design Patterns**: Strategy, Observer, Factory, Singleton, Repository
2. **System Architecture**: Scalable, maintainable messaging system
3. **Concurrent Programming**: Thread-safe operations and graceful shutdown
4. **SOLID Principles**: Clean, extensible object-oriented design
5. **Real-world Problem Solving**: Enterprise messaging system implementation
6. **Clean Architecture**: Separation of concerns with strategy pattern

## 🔧 Recent Improvements

### Architecture Enhancements

- **Robust Topic Management**: Enhanced topic lookup with fallback mechanisms
- **Thread Safety**: All operations properly synchronized
- **Clean Shutdown**: Graceful termination of background threads
- **Memory Efficiency**: Optimized object creation and management

### Performance Optimizations

- **Reduced Logging**: Clean, emoji-enhanced output for better readability
- **Faster Execution**: Optimized sleep times and concurrent operations
- **Resource Cleanup**: Automatic deletion of generated files
- **Error Handling**: Comprehensive error handling with user-friendly messages

---

**Built with ❤️ using Python, advanced design patterns, and concurrent programming techniques**

## 🤝 Contributing

This is an educational project demonstrating LLD principles. Feel free to:

- Add new routing algorithms
- Implement additional delivery guarantees
- Add new persistence backends
- Improve the demo scenarios
- Add comprehensive unit tests

## 📄 License

This project is for educational purposes and demonstrates Low-Level Design principles for software engineering interviews and learning.
