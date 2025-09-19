# HTTP/REST Protocol Example

This directory contains examples of HTTP/REST communication in distributed systems.

## Overview

REST (Representational State Transfer) is an architectural style for distributed systems that uses HTTP methods to perform operations on resources identified by URLs.

## Files

- `server.py` - Flask-based REST API server
- `client.py` - Python client for consuming the REST API
- `README.md` - This documentation file

## Features

### Server (server.py)
- User management endpoints (CRUD operations)
- Message handling endpoints
- JSON request/response format
- Error handling and status codes
- Health check endpoint

### Client (client.py)
- RESTClient class for API interaction
- Demo mode with full API testing
- Interactive mode for manual testing
- Pretty-printed responses

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check and API documentation |
| GET | `/users` | List all users |
| GET | `/users/<id>` | Get specific user |
| POST | `/users` | Create new user |
| PUT | `/users/<id>` | Update user |
| DELETE | `/users/<id>` | Delete user |
| GET | `/messages` | List all messages |
| POST | `/messages` | Send message |

## Running the Examples

### 1. Start the Server
```bash
cd http_rest
python server.py
```

The server will start on `http://localhost:5000`

### 2. Run the Client Demo
```bash
# In another terminal
python client.py
```

### 3. Interactive Client Mode
```bash
python client.py interactive
```

## Example Usage

### Creating a User
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

### Sending a Message
```bash
curl -X POST http://localhost:5000/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello World!", "sender": "John"}'
```

## Key Concepts Demonstrated

1. **RESTful Design**: Resource-based URLs and HTTP methods
2. **JSON Communication**: Structured data exchange
3. **Status Codes**: Proper HTTP status code usage
4. **Error Handling**: Consistent error responses
5. **CRUD Operations**: Create, Read, Update, Delete functionality

## Advantages of HTTP/REST

- ✅ Simple and widely understood
- ✅ Stateless communication
- ✅ Cacheable responses
- ✅ Language and platform agnostic
- ✅ Built-in HTTP features (authentication, compression, etc.)

## Disadvantages of HTTP/REST

- ❌ Higher overhead compared to binary protocols
- ❌ Limited real-time capabilities
- ❌ Multiple round trips for complex operations
- ❌ No built-in schema validation

## Use Cases

- Web APIs and microservices
- CRUD operations on resources
- Integration between different systems
- Mobile app backends
- Public APIs for third-party developers