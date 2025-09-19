#!/usr/bin/env python3
"""
gRPC Server Example
Implementasi server gRPC untuk sistem terdistribusi
"""

import grpc
from concurrent import futures
import threading
import time
from datetime import datetime
import json

# Since we can't generate protobuf files, we'll simulate gRPC-like functionality
# In a real implementation, you would use the generated protobuf files

class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at
        }

class ChatMessage:
    def __init__(self, sender, content, user_id=None):
        self.sender = sender
        self.content = content
        self.timestamp = datetime.now().isoformat()
        self.user_id = user_id or 0
    
    def to_dict(self):
        return {
            "sender": self.sender,
            "content": self.content, 
            "timestamp": self.timestamp,
            "user_id": self.user_id
        }

class MockUserServiceServicer:
    """Mock implementation of gRPC User Service"""
    
    def __init__(self):
        self.users = {
            1: User(1, "Alice", "alice@example.com"),
            2: User(2, "Bob", "bob@example.com")
        }
        self.chat_clients = []  # For bidirectional streaming
        self.next_user_id = 3
    
    def GetUser(self, request_data):
        """Unary RPC - Get single user"""
        user_id = request_data.get('user_id')
        user = self.users.get(user_id)
        
        if user:
            return {"success": True, "user": user.to_dict()}
        else:
            return {"success": False, "error": "User not found"}
    
    def CreateUser(self, request_data):
        """Unary RPC - Create user"""
        name = request_data.get('name')
        email = request_data.get('email')
        
        if not name or not email:
            return {"success": False, "error": "Name and email are required"}
        
        new_user = User(self.next_user_id, name, email)
        self.users[self.next_user_id] = new_user
        self.next_user_id += 1
        
        return {"success": True, "user": new_user.to_dict()}
    
    def UpdateUser(self, request_data):
        """Unary RPC - Update user"""
        user_id = request_data.get('user_id')
        name = request_data.get('name')
        email = request_data.get('email')
        
        user = self.users.get(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        
        if name:
            user.name = name
        if email:
            user.email = email
            
        return {"success": True, "user": user.to_dict()}
    
    def DeleteUser(self, request_data):
        """Unary RPC - Delete user"""
        user_id = request_data.get('user_id')
        
        if user_id in self.users:
            del self.users[user_id]
            return {"success": True, "message": "User deleted successfully"}
        else:
            return {"success": False, "error": "User not found"}
    
    def ListUsers(self, request_data):
        """Server streaming RPC - List users with streaming"""
        limit = request_data.get('limit', 10)
        offset = request_data.get('offset', 0)
        
        users_list = list(self.users.values())[offset:offset+limit]
        
        # Simulate streaming by yielding one user at a time
        for user in users_list:
            yield {"success": True, "user": user.to_dict()}
    
    def CreateUsers(self, requests_stream):
        """Client streaming RPC - Create multiple users"""
        created_users = []
        
        for request_data in requests_stream:
            name = request_data.get('name')
            email = request_data.get('email')
            
            if name and email:
                new_user = User(self.next_user_id, name, email)
                self.users[self.next_user_id] = new_user
                created_users.append(new_user)
                self.next_user_id += 1
        
        return {
            "success": True,
            "created_count": len(created_users),
            "users": [user.to_dict() for user in created_users]
        }
    
    def ChatStream(self, message_stream):
        """Bidirectional streaming RPC - Chat functionality"""
        client_id = len(self.chat_clients)
        self.chat_clients.append(client_id)
        
        try:
            for message_data in message_stream:
                # Broadcast message to all clients
                chat_message = ChatMessage(
                    message_data.get('sender', 'anonymous'),
                    message_data.get('content', ''),
                    message_data.get('user_id', 0)
                )
                
                # In real gRPC, this would be sent to all connected clients
                yield {"success": True, "message": chat_message.to_dict()}
                
        finally:
            if client_id in self.chat_clients:
                self.chat_clients.remove(client_id)

class MockGRPCServer:
    """Mock gRPC server implementation"""
    
    def __init__(self, port=50051):
        self.port = port
        self.servicer = MockUserServiceServicer()
        self.running = False
        self.server_thread = None
    
    def start(self):
        """Start the mock gRPC server"""
        self.running = True
        self.server_thread = threading.Thread(target=self._run_server)
        self.server_thread.start()
        print(f"🚀 Mock gRPC Server started on port {self.port}")
        print("Available methods:")
        print("- GetUser(user_id)")
        print("- CreateUser(name, email)")
        print("- UpdateUser(user_id, name, email)")
        print("- DeleteUser(user_id)")
        print("- ListUsers(limit, offset)")
        print("- CreateUsers(users_stream)")
        print("- ChatStream(message_stream)")
        
    def _run_server(self):
        """Internal server loop"""
        try:
            while self.running:
                time.sleep(1)  # Keep server alive
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.server_thread:
            self.server_thread.join()
        print("🛑 Mock gRPC Server stopped")
    
    def handle_request(self, method, request_data):
        """Handle incoming requests"""
        if not self.running:
            return {"success": False, "error": "Server not running"}
        
        try:
            if method == "GetUser":
                return self.servicer.GetUser(request_data)
            elif method == "CreateUser":
                return self.servicer.CreateUser(request_data)
            elif method == "UpdateUser":
                return self.servicer.UpdateUser(request_data)
            elif method == "DeleteUser":
                return self.servicer.DeleteUser(request_data)
            elif method == "ListUsers":
                # For streaming, we'll return a list instead of generator for simplicity
                return list(self.servicer.ListUsers(request_data))
            else:
                return {"success": False, "error": f"Unknown method: {method}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

def main():
    """Main server function"""
    server = MockGRPCServer()
    
    try:
        server.start()
        
        print("\nServer Status: Running ✅")
        print("Press Ctrl+C to stop the server...")
        
        # Keep the main thread alive
        while server.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🔴 Shutting down server...")
        server.stop()
        print("Server stopped gracefully.")

if __name__ == '__main__':
    main()