# Distributed Systems Communication Protocols
## Repositori untuk Sistem Terdistribusi dari Berbagai Macam Protokol Komunikasi

This repository demonstrates various communication protocols used in distributed systems, providing practical examples and implementations for learning and reference purposes.

## 🌐 Communication Protocols Implemented

### 1. HTTP/REST API
- Simple client-server communication
- RESTful service examples
- JSON data exchange
- Status codes and error handling

### 2. gRPC (Google Remote Procedure Call)
- High-performance RPC framework
- Protocol buffer definitions
- Bidirectional streaming
- Cross-language compatibility

### 3. WebSocket
- Real-time bidirectional communication
- Persistent connections
- Chat application example
- Live data streaming

### 4. Message Queues
- **RabbitMQ**: Reliable message broker
- **Redis Pub/Sub**: High-performance messaging
- Asynchronous communication patterns
- Work queue implementations

### 5. TCP Sockets
- Low-level socket programming
- Custom protocol implementation
- Binary data transmission
- Connection management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker and Docker Compose
- Git

### Installation
```bash
git clone https://github.com/luthfizahrane/dist_sys.git
cd dist_sys
pip install -r requirements.txt
```

### Running Examples
Each protocol has its own directory with specific instructions:

```bash
# HTTP/REST Example
cd http_rest
python server.py &
python client.py

# gRPC Example
cd grpc
python server.py &
python client.py

# WebSocket Example
cd websocket
python server.py &
python client.py

# Message Queue Example
cd message_queue
docker-compose up -d
python producer.py &
python consumer.py

# TCP Socket Example
cd tcp_socket
python server.py &
python client.py
```

## 📁 Project Structure

```
dist_sys/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── http_rest/
│   ├── server.py
│   ├── client.py
│   └── README.md
├── grpc/
│   ├── server.py
│   ├── client.py
│   ├── protos/
│   └── README.md
├── websocket/
│   ├── server.py
│   ├── client.py
│   └── README.md
├── message_queue/
│   ├── rabbitmq/
│   ├── redis/
│   └── README.md
├── tcp_socket/
│   ├── server.py
│   ├── client.py
│   └── README.md
└── docs/
    ├── performance_comparison.md
    └── use_cases.md
```

## 🔄 Communication Patterns

- **Synchronous**: HTTP/REST, gRPC, TCP Sockets
- **Asynchronous**: Message Queues, WebSocket events
- **Request-Response**: HTTP, gRPC, TCP
- **Publish-Subscribe**: Message Queues, WebSocket broadcasting
- **Streaming**: gRPC streams, WebSocket continuous data

## 📊 Performance Characteristics

| Protocol | Latency | Throughput | Overhead | Use Case |
|----------|---------|------------|----------|----------|
| HTTP/REST | Medium | Medium | High | Web APIs, CRUD operations |
| gRPC | Low | High | Low | Microservices, Internal APIs |
| WebSocket | Low | High | Low | Real-time apps, Gaming |
| Message Queue | Medium | Very High | Medium | Async processing, Decoupling |
| TCP Socket | Very Low | Very High | Very Low | High-performance, Custom protocols |

## 🛠️ Development

### Adding New Protocols
1. Create a new directory for the protocol
2. Implement server and client examples
3. Add documentation and README
4. Update main README with protocol information
5. Add Docker support if applicable

### Testing
```bash
# Run all protocol tests
python -m pytest tests/

# Test specific protocol
python -m pytest tests/test_http_rest.py
```

## 📚 Learning Resources

- [Distributed Systems Concepts](docs/concepts.md)
- [Protocol Comparison Guide](docs/performance_comparison.md)
- [Use Case Examples](docs/use_cases.md)
- [Best Practices](docs/best_practices.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests and documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Inspired by distributed systems courses and real-world implementations
- Community contributions and feedback
- Open source libraries and frameworks used in examples

---

**Catatan dalam Bahasa Indonesia:**
Repositori ini menyediakan contoh implementasi berbagai protokol komunikasi dalam sistem terdistribusi. Setiap protokol memiliki contoh server dan client yang dapat dipelajari dan dimodifikasi sesuai kebutuhan. Dokumentasi lengkap tersedia dalam setiap direktori protokol.