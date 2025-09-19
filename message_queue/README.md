# Message Queue Protocol Examples

This directory contains examples of asynchronous messaging using message queue systems for distributed applications.

## Overview

Message queues provide asynchronous communication between distributed system components through a message broker. They enable loose coupling, scalability, and fault tolerance by decoupling producers and consumers of messages.

## Directory Structure

```
message_queue/
├── redis/
│   ├── publisher.py    # Redis Pub/Sub publisher
│   └── subscriber.py   # Redis Pub/Sub subscriber
├── rabbitmq/          # RabbitMQ examples (future implementation)
└── README.md          # This file
```

## Message Queue Patterns

### 1. Publish/Subscribe (Pub/Sub)
- Publishers send messages to channels/topics
- Subscribers receive messages from channels they're subscribed to
- One-to-many communication pattern
- Messages are not persisted after delivery

### 2. Work Queues (Task Distribution)
- Producers send tasks to queues
- Workers consume tasks from queues
- One-to-one communication pattern
- Load balancing among workers

### 3. Request/Reply
- Client sends request and waits for response
- Server processes request and sends reply
- Correlation IDs to match requests with responses
- Point-to-point communication

## Redis Pub/Sub Implementation

### Features
- **Publisher** (`redis/publisher.py`):
  - Publish messages to multiple channels
  - Batch message publishing
  - Periodic message publishing
  - Publisher statistics and metrics
  - Interactive publishing mode

- **Subscriber** (`redis/subscriber.py`):
  - Subscribe to multiple channels simultaneously
  - Real-time message processing
  - Message filtering and routing
  - Subscriber statistics
  - Interactive subscription management

### Message Format
```json
{
  "type": "message_type",
  "content": "message content",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "sender": "publisher_id",
  "metadata": {
    "priority": "high",
    "category": "alerts"
  }
}
```

## Running Redis Examples

### Prerequisites
```bash
# Start Redis server
docker run -d -p 6379:6379 redis:alpine

# Or using docker-compose
docker-compose up redis
```

### 1. Start Subscriber
```bash
cd message_queue/redis
python subscriber.py
```

### 2. Start Publisher
```bash
# In another terminal
python publisher.py
```

### 3. Interactive Modes
```bash
# Interactive subscriber
python subscriber.py interactive

# Interactive publisher
python publisher.py interactive
```

## Usage Examples

### Basic Publisher
```python
from redis.publisher import MockRedisPublisher

publisher = MockRedisPublisher()
publisher.connect()

# Publish single message
publisher.publish('news', {
    'title': 'Breaking News',
    'content': 'Important update!',
    'priority': 'high'
})

# Publish multiple messages
messages = [
    ('alerts', {'type': 'warning', 'message': 'CPU usage high'}),
    ('logs', {'level': 'info', 'message': 'Application started'})
]
publisher.publish_multiple(messages)

publisher.disconnect()
```

### Basic Subscriber
```python
from redis.subscriber import MockRedisSubscriber

subscriber = MockRedisSubscriber()

def on_message(message):
    channel = message['channel']
    data = message['data']
    print(f"Received on {channel}: {data}")

subscriber.set_message_callback(on_message)
subscriber.connect()
subscriber.subscribe('news', 'alerts', 'logs')
subscriber.listen()

# Keep running until Ctrl+C
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    subscriber.disconnect()
```

## Channel Organization

### Recommended Channel Patterns

#### 1. By Service
```
user-service.events
order-service.events
payment-service.events
```

#### 2. By Event Type
```
user.created
user.updated
user.deleted
order.placed
order.shipped
```

#### 3. By Priority/Level
```
alerts.critical
alerts.warning
alerts.info
logs.error
logs.debug
```

#### 4. By Environment
```
prod.alerts
staging.alerts
dev.logs
```

## Message Types and Examples

### 1. Event Notifications
```json
{
  "type": "user.created",
  "user_id": 12345,
  "email": "user@example.com",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "metadata": {
    "source": "user-service",
    "version": "v1.0"
  }
}
```

### 2. System Alerts
```json
{
  "type": "system.alert",
  "level": "critical",
  "message": "Database connection failed",
  "service": "user-service",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "details": {
    "error_code": "DB_CONNECTION_FAILED",
    "retry_count": 3
  }
}
```

### 3. Application Logs
```json
{
  "type": "application.log",
  "level": "info",
  "message": "User authentication successful",
  "user_id": 12345,
  "timestamp": "2024-01-01T12:00:00.000Z",
  "context": {
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0..."
  }
}
```

### 4. Business Events
```json
{
  "type": "order.placed",
  "order_id": "ORD-123456",
  "customer_id": 78901,
  "total_amount": 99.99,
  "timestamp": "2024-01-01T12:00:00.000Z",
  "items": [
    {"product_id": "PROD-001", "quantity": 2, "price": 49.99}
  ]
}
```

## Performance Characteristics

### Redis Pub/Sub
- **Latency**: 5-50ms (including broker processing)
- **Throughput**: 50,000+ messages/second
- **Memory Usage**: Messages not persisted
- **Scalability**: Excellent for real-time notifications

### Message Size Impact
- **Small messages (< 1KB)**: 8,000 msg/sec
- **Medium messages (1-10KB)**: 6,000 msg/sec
- **Large messages (> 100KB)**: 2,000 msg/sec

## Interactive Commands

### Publisher Commands
- `pub <channel> <message>` - Publish message to channel
- `batch` - Publish batch of test messages
- `periodic <channel> <interval> <count>` - Periodic publishing
- `stats` - Show publisher statistics
- `exit` - Exit publisher mode

### Subscriber Commands
- `sub <channel1> [channel2] ...` - Subscribe to channels
- `unsub <channel1> [channel2] ...` - Unsubscribe from channels
- `listen` - Start listening for messages
- `stop` - Stop listening
- `inject <channel> <message>` - Inject test message
- `stats` - Show subscriber statistics
- `exit` - Exit subscriber mode

## Key Concepts Demonstrated

1. **Asynchronous Communication**: Non-blocking message exchange
2. **Loose Coupling**: Publishers and subscribers are independent
3. **Scalability**: Multiple publishers and subscribers
4. **Message Broadcasting**: One-to-many communication
5. **Channel Management**: Topic-based message routing
6. **Error Handling**: Connection failures and recovery

## Advantages of Message Queues

- ✅ Decoupling of system components
- ✅ Asynchronous processing capabilities
- ✅ Horizontal scalability
- ✅ Fault tolerance and reliability
- ✅ Load balancing among consumers
- ✅ Message persistence (broker-dependent)
- ✅ Built-in retry mechanisms

## Disadvantages of Message Queues

- ❌ Additional infrastructure complexity
- ❌ Potential single point of failure (broker)
- ❌ Message ordering challenges
- ❌ Debugging distributed flows
- ❌ Network partitioning issues
- ❌ Message delivery guarantees complexity

## Use Cases

### Ideal For:
- Event-driven architectures
- Microservices communication
- Background job processing
- System notifications and alerts
- Data pipeline processing
- Real-time analytics
- Workflow orchestration

### Message Queue Patterns:
- **Fan-out**: One publisher, multiple subscribers
- **Work distribution**: Multiple workers processing tasks
- **Event sourcing**: Capturing all system events
- **CQRS**: Command and Query Responsibility Segregation

## Production Considerations

### High Availability
- Use Redis Cluster or Sentinel for fault tolerance
- Implement publisher/subscriber reconnection logic
- Set up monitoring and alerting
- Configure appropriate timeouts

### Performance Optimization
- Use connection pooling
- Implement message batching
- Optimize message serialization
- Monitor queue sizes and processing rates

### Security
- Enable Redis AUTH for authentication
- Use TLS for encrypted connections
- Implement access control lists (ACLs)
- Network security (VPC, firewalls)

### Monitoring
- Track message throughput and latency
- Monitor queue depths and processing times
- Alert on connection failures
- Log important events for troubleshooting

## Future Implementations

### RabbitMQ Examples (Planned)
- Work queues with task distribution
- Message persistence and durability
- Complex routing with exchanges
- Dead letter queues for error handling

### Apache Kafka Examples (Planned)
- High-throughput event streaming
- Partitioned topics for scalability
- Consumer groups for parallel processing
- Event sourcing patterns

## Integration Patterns

Message queues work well with other protocols:
- **HTTP/REST**: Trigger async processing via REST endpoints
- **gRPC**: Use streaming for real-time message delivery
- **WebSocket**: Push queue messages to web clients
- **TCP Sockets**: High-performance message processing

This message queue implementation provides the foundation for building scalable, decoupled distributed systems with reliable asynchronous communication.