# gRPC Protocol Example

This directory contains examples of gRPC communication in distributed systems.

## Overview

gRPC (gRPC Remote Procedure Calls) is a high-performance, open-source universal RPC framework that uses HTTP/2 for transport, Protocol Buffers as the interface description language, and provides features such as authentication, bidirectional streaming, flow control, and more.

## Files

- `server.py` - Mock gRPC server implementation
- `client.py` - Python client for gRPC services
- `protos/service.proto` - Protocol Buffer definitions
- `README.md` - This documentation file

## Features

### Server (server.py)
- Mock implementation of gRPC UserService
- Supports all RPC patterns:
  - Unary RPC (single request, single response)
  - Server streaming RPC (single request, stream of responses)
  - Client streaming RPC (stream of requests, single response)
  - Bidirectional streaming RPC (stream of requests and responses)
- User management operations
- Chat functionality with streaming

### Client (client.py)
- Comprehensive gRPC client implementation
- Demo mode showing all RPC patterns
- Interactive mode for manual testing
- Connection management and error handling

## RPC Patterns Demonstrated

### 1. Unary RPC
```python
# Single request, single response
response = client.get_user(1)
```

### 2. Server Streaming RPC
```python
# Single request, stream of responses
for user_response in client.list_users(limit=5):
    print(user_response)
```

### 3. Client Streaming RPC
```python
# Stream of requests, single response
users_to_create = [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"}
]
response = client.create_users_batch(users_to_create)
```

### 4. Bidirectional Streaming RPC
```python
# Stream of requests and responses
chat_messages = [
    {"sender": "Client", "content": "Hello!"},
    {"sender": "Client", "content": "How are you?"}
]
for response in client.chat_stream(chat_messages):
    print(response)
```

## Running the Examples

### 1. Start the Server
```bash
cd grpc
python server.py
```

### 2. Run the Client Demo
```bash
# In another terminal
python client.py
```

### 3. Interactive Client Mode
```bash
python client.py interactive
```

## Protocol Buffer Definition

The `service.proto` file defines the gRPC service interface:

```protobuf
service UserService {
  rpc GetUser(GetUserRequest) returns (UserResponse);
  rpc CreateUser(CreateUserRequest) returns (UserResponse);
  rpc ListUsers(ListUsersRequest) returns (stream UserResponse);
  rpc CreateUsers(stream CreateUserRequest) returns (CreateUsersResponse);
  rpc ChatStream(stream ChatMessage) returns (stream ChatMessage);
}
```

## Mock Implementation Note

This implementation uses a mock gRPC approach since we couldn't install the full gRPC tools. In a real deployment:

1. Generate Python code from `.proto` files:
```bash
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --proto_path=protos protos/service.proto
```

2. Import the generated modules:
```python
import service_pb2
import service_pb2_grpc
```

3. Implement actual gRPC server and client using the generated stubs.

## Key Concepts Demonstrated

1. **RPC Patterns**: All four gRPC communication patterns
2. **Streaming**: Both client and server-side streaming
3. **Protocol Buffers**: Structured data definition
4. **Connection Management**: Persistent HTTP/2 connections
5. **Error Handling**: Graceful error management
6. **Concurrent Operations**: Multiple simultaneous RPC calls

## Advantages of gRPC

- ✅ High performance with HTTP/2 and Protocol Buffers
- ✅ Strong typing with schema definitions
- ✅ Support for multiple programming languages
- ✅ Built-in streaming support
- ✅ Automatic code generation
- ✅ Built-in authentication and encryption
- ✅ Load balancing and service discovery

## Disadvantages of gRPC

- ❌ More complex than REST
- ❌ Limited browser support
- ❌ Binary protocol (not human-readable)
- ❌ Learning curve for Protocol Buffers
- ❌ Debugging can be more difficult

## Use Cases

- Internal microservice communication
- High-performance APIs
- Real-time streaming applications
- Multi-language distributed systems
- APIs requiring strong typing
- Systems with high throughput requirements

## Production Considerations

- Implement proper authentication (JWT, TLS certificates)
- Use connection pooling for clients
- Configure appropriate timeouts and retries
- Monitor RPC metrics (latency, error rates)
- Implement circuit breakers for resilience
- Use load balancing for high availability