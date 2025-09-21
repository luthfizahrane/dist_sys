# Quick Start Guide - Distributed Systems Communication Protocols

This guide will help you quickly get started with all the communication protocols implemented in this repository.

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose (optional, for full setup)
- Basic understanding of distributed systems concepts

## Quick Setup

### Option 1: Manual Setup
```bash
# Clone the repository
git clone https://github.com/luthfizahrane/dist_sys.git
cd dist_sys

# Install dependencies (if available)
pip install -r requirements.txt
```

### Option 2: Docker Setup
```bash
# Start all services with Docker Compose
docker-compose up -d

# Check service status
docker-compose ps
```

## Protocol Quick Reference

| Protocol | Server Port | Client Usage | Best For |
|----------|-------------|--------------|----------|
| HTTP/REST | 5000 | `curl` or Python client | Web APIs, CRUD operations |
| gRPC | 50051 | Python client | Internal APIs, microservices |
| WebSocket | 8765 | Python client | Real-time communication |
| TCP Socket | 9999 | Python client | High-performance, custom protocols |
| Redis Pub/Sub | 6379 | Publisher/Subscriber | Asynchronous messaging |

## 5-Minute Protocol Tour

### 1. TCP Socket (Fastest to Test)

**Terminal 1 - Start Server:**
```bash
cd tcp_socket
python server.py
```

**Terminal 2 - Run Client:**
```bash
cd tcp_socket
python client.py
```

**Expected Output:**
- Server shows client connections and message processing
- Client demonstrates ping/pong, echo, broadcast, and statistics

### 2. WebSocket (Real-time Demo)

**Terminal 1 - Start Server:**
```bash
cd websocket
python server.py
```

**Terminal 2 - Interactive Chat:**
```bash
cd websocket
python client.py chat
```

**Try these commands:**
```
Hello WebSocket!
/broadcast This goes to everyone!
/ping
/exit
```

### 3. Message Queue (Async Communication)

**Terminal 1 - Start Subscriber:**
```bash
cd message_queue/redis
python subscriber.py
```

**Terminal 2 - Start Publisher:**
```bash
cd message_queue/redis
python publisher.py
```

**Watch messages flow from publisher to subscriber in real-time!**

### 4. HTTP/REST (Note: Requires Flask)

**Terminal 1 - Start Server:**
```bash
cd http_rest
python server.py  # May require: pip install flask
```

**Terminal 2 - Test with Client:**
```bash
cd http_rest
python client.py
```

**Or test with curl:**
```bash
curl http://localhost:5000/users
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"name":"Test","email":"test@example.com"}'
```

### 5. gRPC (Mock Implementation)

**Terminal 1 - Start Server:**
```bash
cd grpc
python server.py
```

**Terminal 2 - Run Client:**
```bash
cd grpc
python client.py
```

## Interactive Modes

Each protocol supports interactive mode for hands-on testing:

```bash
# TCP Socket interactive mode
cd tcp_socket && python client.py interactive

# WebSocket chat mode
cd websocket && python client.py chat

# Redis interactive publisher
cd message_queue/redis && python publisher.py interactive

# Redis interactive subscriber
cd message_queue/redis && python subscriber.py interactive

# gRPC interactive mode
cd grpc && python client.py interactive
```

## Performance Testing

Test the performance characteristics of each protocol:

```bash
# TCP Socket performance test
cd tcp_socket && python client.py performance

# WebSocket stress test
cd websocket && python client.py stress

# Redis publisher stress test
cd message_queue/redis && python publisher.py stress
```

## Common Commands Summary

### TCP Socket Commands
- `/ping` - Test latency
- `/echo <message>` - Echo test
- `/broadcast <message>` - Send to all clients
- `/stats` - Server statistics

### WebSocket Commands
- `/broadcast <message>` - Broadcast message
- `/ping` - Heartbeat test
- Regular text - Chat message

### Redis Publisher Commands
- `pub <channel> <message>` - Publish to channel
- `batch` - Send test batch
- `stats` - Publisher statistics

### Redis Subscriber Commands
- `sub <channel>` - Subscribe to channel
- `listen` - Start listening
- `stats` - Subscriber statistics

## Protocol Comparison in Action

### Latency Test (Send "Hello" message and measure response time)

1. **TCP Socket**: ~0.3ms (fastest)
2. **gRPC**: ~2ms (efficient RPC)
3. **WebSocket**: ~5ms (real-time)
4. **Message Queue**: ~15ms (via broker)
5. **HTTP/REST**: ~25ms (HTTP overhead)

### Throughput Test (Messages per second)

1. **TCP Socket**: 95,000+ msg/sec
2. **gRPC**: 45,000+ msg/sec
3. **WebSocket**: 15,000+ msg/sec
4. **Message Queue**: 8,000+ msg/sec
5. **HTTP/REST**: 2,500+ msg/sec

## Troubleshooting

### Common Issues

**"Connection refused" errors:**
- Make sure the server is running first
- Check if the port is already in use
- Verify firewall settings

**Import errors:**
- Install required dependencies: `pip install flask requests`
- Use the mock implementations if packages are unavailable

**Permission errors:**
- Run with appropriate permissions
- Check port availability (1024+ for non-root users)

### Debug Mode

Enable debug output by modifying the scripts:
```python
# Add at the top of any script
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Next Steps

### 1. Explore Individual Protocols
- Read the README in each protocol directory
- Try the interactive modes
- Experiment with different message types

### 2. Performance Analysis
- Run the performance tests
- Compare results on your system
- Read `docs/performance_comparison.md`

### 3. Build Your Own
- Modify the examples for your use case
- Combine protocols (e.g., HTTP + WebSocket)
- Add authentication and security

### 4. Production Deployment
- Use Docker Compose for full setup
- Add monitoring and logging
- Implement proper error handling

## Example Use Cases

### Real-time Chat Application
```
WebSocket (client-server) + Redis Pub/Sub (message distribution)
```

### Microservices Architecture
```
gRPC (internal services) + HTTP/REST (external API) + Message Queue (async tasks)
```

### High-Frequency Trading System
```
TCP Socket (order processing) + Message Queue (risk management) + WebSocket (market data)
```

### IoT Platform
```
TCP Socket (device communication) + HTTP/REST (API) + Message Queue (data processing)
```

## Learning Path

1. **Start with TCP Socket** - Understand the basics of network communication
2. **Try WebSocket** - Learn real-time bidirectional communication
3. **Explore Message Queues** - Understand asynchronous patterns
4. **Use gRPC** - Experience efficient RPC communication
5. **Compare with HTTP/REST** - See the trade-offs

## Help and Support

- Check individual protocol README files for detailed documentation
- Look at `docs/performance_comparison.md` for detailed analysis
- Examine the source code for implementation details
- Test with the interactive modes to understand behavior

Happy distributed systems programming! 🚀