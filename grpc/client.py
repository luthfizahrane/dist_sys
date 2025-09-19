#!/usr/bin/env python3
"""
gRPC Client Example
Implementasi client gRPC untuk mengakses server
"""

import json
import time
import threading
from datetime import datetime

class MockGRPCClient:
    """Mock gRPC client implementation"""
    
    def __init__(self, server_address="localhost:50051"):
        self.server_address = server_address
        self.connected = False
        # In real gRPC, this would establish a channel to the server
        # For this mock, we'll simulate the connection
        
    def connect(self):
        """Connect to the gRPC server"""
        try:
            # Simulate connection
            self.connected = True
            print(f"✅ Connected to gRPC server at {self.server_address}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the server"""
        self.connected = False
        print("🔌 Disconnected from gRPC server")
    
    def _make_request(self, method, request_data):
        """Simulate making a gRPC request"""
        if not self.connected:
            return {"success": False, "error": "Not connected to server"}
        
        # In real implementation, this would send the request over the network
        # For demo purposes, we'll simulate the server response
        return self._simulate_server_response(method, request_data)
    
    def _simulate_server_response(self, method, request_data):
        """Simulate server responses for demo purposes"""
        # This is a mock - in real gRPC, this would come from the actual server
        if method == "GetUser":
            user_id = request_data.get('user_id')
            if user_id in [1, 2]:
                return {
                    "success": True,
                    "user": {
                        "user_id": user_id,
                        "name": "Alice" if user_id == 1 else "Bob",
                        "email": f"{'alice' if user_id == 1 else 'bob'}@example.com",
                        "created_at": datetime.now().isoformat()
                    }
                }
            else:
                return {"success": False, "error": "User not found"}
        
        elif method == "CreateUser":
            return {
                "success": True,
                "user": {
                    "user_id": 3,
                    "name": request_data.get('name'),
                    "email": request_data.get('email'),
                    "created_at": datetime.now().isoformat()
                }
            }
        
        elif method == "ListUsers":
            return [
                {
                    "success": True,
                    "user": {
                        "user_id": 1,
                        "name": "Alice",
                        "email": "alice@example.com",
                        "created_at": datetime.now().isoformat()
                    }
                },
                {
                    "success": True,
                    "user": {
                        "user_id": 2,
                        "name": "Bob", 
                        "email": "bob@example.com",
                        "created_at": datetime.now().isoformat()
                    }
                }
            ]
        
        else:
            return {"success": True, "message": f"Mock response for {method}"}
    
    # Unary RPC methods
    def get_user(self, user_id):
        """Get a single user by ID"""
        request_data = {"user_id": user_id}
        return self._make_request("GetUser", request_data)
    
    def create_user(self, name, email):
        """Create a new user"""
        request_data = {"name": name, "email": email}
        return self._make_request("CreateUser", request_data)
    
    def update_user(self, user_id, name=None, email=None):
        """Update an existing user"""
        request_data = {"user_id": user_id}
        if name:
            request_data["name"] = name
        if email:
            request_data["email"] = email
        return self._make_request("UpdateUser", request_data)
    
    def delete_user(self, user_id):
        """Delete a user"""
        request_data = {"user_id": user_id}
        return self._make_request("DeleteUser", request_data)
    
    # Server streaming RPC
    def list_users(self, limit=10, offset=0):
        """List users with server streaming"""
        request_data = {"limit": limit, "offset": offset}
        response = self._make_request("ListUsers", request_data)
        
        # Simulate streaming by yielding results
        if isinstance(response, list):
            for user_response in response:
                yield user_response
        else:
            yield response
    
    # Client streaming RPC
    def create_users_batch(self, users_data):
        """Create multiple users using client streaming"""
        print("📤 Starting client streaming - Create Users Batch")
        
        # Simulate sending stream of requests
        for i, user_data in enumerate(users_data):
            print(f"   Sending user {i+1}: {user_data}")
            time.sleep(0.1)  # Simulate network delay
        
        # Simulate server response after processing all requests
        return {
            "success": True,
            "created_count": len(users_data),
            "users": [
                {
                    "user_id": i + 10,
                    "name": user_data["name"],
                    "email": user_data["email"],
                    "created_at": datetime.now().isoformat()
                }
                for i, user_data in enumerate(users_data)
            ]
        }
    
    # Bidirectional streaming RPC
    def chat_stream(self, messages_to_send):
        """Bidirectional streaming chat"""
        print("💬 Starting bidirectional streaming - Chat")
        
        def send_messages():
            for message in messages_to_send:
                print(f"   📤 Sending: {message}")
                time.sleep(1)
        
        def receive_messages():
            # Simulate receiving messages
            responses = [
                {"sender": "Server", "content": f"Echo: {msg['content']}", "timestamp": datetime.now().isoformat()}
                for msg in messages_to_send
            ]
            
            for response in responses:
                time.sleep(0.5)
                print(f"   📥 Received: {response}")
                yield response
        
        # Start sending in background
        send_thread = threading.Thread(target=send_messages)
        send_thread.start()
        
        # Receive messages
        for response in receive_messages():
            yield response
        
        send_thread.join()

def print_response(operation, response):
    """Pretty print gRPC response"""
    print(f"\n{'='*60}")
    print(f"🔧 Operation: {operation}")
    print(f"📝 Response:")
    print(json.dumps(response, indent=2))
    print(f"{'='*60}")

def demo_grpc_client():
    """Demonstrate gRPC client functionality"""
    print("gRPC Client Demo")
    print("================")
    
    client = MockGRPCClient()
    
    if not client.connect():
        print("❌ Cannot connect to server. Please start the server first:")
        print("   python server.py")
        return
    
    try:
        # Unary RPC calls
        print("\n🔵 Unary RPC Examples")
        
        # Get user
        response = client.get_user(1)
        print_response("Get User (ID: 1)", response)
        
        # Create user
        response = client.create_user("Charlie Brown", "charlie@example.com")
        print_response("Create User", response)
        
        # Update user
        response = client.update_user(1, name="Alice Updated")
        print_response("Update User", response)
        
        # Server streaming RPC
        print("\n🟢 Server Streaming RPC Example")
        print("📡 Listing users with streaming...")
        
        for i, user_response in enumerate(client.list_users(limit=5)):
            print(f"   Stream response {i+1}: {user_response}")
            time.sleep(0.2)  # Simulate processing time
        
        # Client streaming RPC
        print("\n🟡 Client Streaming RPC Example")
        
        users_to_create = [
            {"name": "David", "email": "david@example.com"},
            {"name": "Eve", "email": "eve@example.com"},
            {"name": "Frank", "email": "frank@example.com"}
        ]
        
        response = client.create_users_batch(users_to_create)
        print_response("Create Users Batch", response)
        
        # Bidirectional streaming RPC
        print("\n🔴 Bidirectional Streaming RPC Example")
        
        chat_messages = [
            {"sender": "Client", "content": "Hello Server!"},
            {"sender": "Client", "content": "How are you?"},
            {"sender": "Client", "content": "gRPC is awesome!"}
        ]
        
        print("💬 Starting chat stream...")
        for response in client.chat_stream(chat_messages):
            pass  # Responses are already printed in the method
        
        print("\n🎉 All gRPC patterns demonstrated successfully!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
    
    finally:
        client.disconnect()

def interactive_mode():
    """Interactive mode for testing gRPC"""
    client = MockGRPCClient()
    
    if not client.connect():
        print("❌ Cannot connect to server")
        return
    
    print("\n🔧 Interactive gRPC Client Mode")
    print("Available commands:")
    print("1. get <user_id> - Get user by ID")
    print("2. create <name> <email> - Create new user")
    print("3. update <user_id> <name> <email> - Update user")
    print("4. delete <user_id> - Delete user")
    print("5. list [limit] - List users (server streaming)")
    print("6. batch - Create users in batch (client streaming)")
    print("7. chat - Start chat session (bidirectional streaming)")
    print("8. exit - Exit interactive mode")
    
    try:
        while True:
            command = input("\ngRPC> ").strip().split()
            if not command:
                continue
            
            cmd = command[0].lower()
            
            if cmd == 'exit':
                break
            elif cmd == 'get' and len(command) > 1:
                user_id = int(command[1])
                response = client.get_user(user_id)
                print(json.dumps(response, indent=2))
            elif cmd == 'create' and len(command) > 2:
                name, email = command[1], command[2]
                response = client.create_user(name, email)
                print(json.dumps(response, indent=2))
            elif cmd == 'list':
                limit = int(command[1]) if len(command) > 1 else 10
                print("📡 Streaming users...")
                for user_response in client.list_users(limit=limit):
                    print(f"  {json.dumps(user_response, indent=2)}")
            elif cmd == 'batch':
                users_data = [
                    {"name": "Interactive1", "email": "int1@example.com"},
                    {"name": "Interactive2", "email": "int2@example.com"}
                ]
                response = client.create_users_batch(users_data)
                print(json.dumps(response, indent=2))
            elif cmd == 'chat':
                messages = [
                    {"sender": "Interactive", "content": "Hello from interactive mode!"}
                ]
                for response in client.chat_stream(messages):
                    pass  # Already printed
            else:
                print("❌ Invalid command. Type 'exit' to quit.")
                
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        client.disconnect()
        print("\n👋 Goodbye!")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        interactive_mode()
    else:
        demo_grpc_client()