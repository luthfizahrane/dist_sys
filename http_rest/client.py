#!/usr/bin/env python3
"""
HTTP/REST Client Example
Implementasi client untuk mengakses REST API server
"""

import requests
import json
import time
from datetime import datetime

class RESTClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self):
        """Check if server is running"""
        try:
            response = self.session.get(f"{self.base_url}/")
            return response.status_code == 200, response.json()
        except requests.exceptions.ConnectionError:
            return False, {"error": "Cannot connect to server"}
    
    def get_users(self):
        """Get all users"""
        response = self.session.get(f"{self.base_url}/users")
        return response.status_code, response.json()
    
    def get_user(self, user_id):
        """Get specific user"""
        response = self.session.get(f"{self.base_url}/users/{user_id}")
        return response.status_code, response.json()
    
    def create_user(self, name, email):
        """Create new user"""
        data = {"name": name, "email": email}
        response = self.session.post(f"{self.base_url}/users", json=data)
        return response.status_code, response.json()
    
    def update_user(self, user_id, name=None, email=None):
        """Update existing user"""
        data = {}
        if name:
            data["name"] = name
        if email:
            data["email"] = email
        
        response = self.session.put(f"{self.base_url}/users/{user_id}", json=data)
        return response.status_code, response.json()
    
    def delete_user(self, user_id):
        """Delete user"""
        response = self.session.delete(f"{self.base_url}/users/{user_id}")
        return response.status_code, response.json()
    
    def get_messages(self):
        """Get all messages"""
        response = self.session.get(f"{self.base_url}/messages")
        return response.status_code, response.json()
    
    def send_message(self, content, sender=None):
        """Send a message"""
        data = {"content": content}
        if sender:
            data["sender"] = sender
        
        response = self.session.post(f"{self.base_url}/messages", json=data)
        return response.status_code, response.json()

def print_response(operation, status_code, data):
    """Pretty print API response"""
    print(f"\n{'='*50}")
    print(f"Operation: {operation}")
    print(f"Status Code: {status_code}")
    print(f"Response: {json.dumps(data, indent=2)}")
    print(f"{'='*50}")

def demo_rest_api():
    """Demonstrate REST API functionality"""
    client = RESTClient()
    
    print("HTTP/REST Client Demo")
    print("====================")
    
    # Health check
    is_healthy, health_data = client.health_check()
    print_response("Health Check", 200 if is_healthy else 500, health_data)
    
    if not is_healthy:
        print("❌ Server is not running. Please start the server first:")
        print("   python server.py")
        return
    
    print("✅ Server is running!")
    
    # Get all users
    status, users = client.get_users()
    print_response("Get All Users", status, users)
    
    # Get specific user
    status, user = client.get_user(1)
    print_response("Get User 1", status, user)
    
    # Create new user
    status, new_user = client.create_user("Charlie", "charlie@example.com")
    print_response("Create User", status, new_user)
    
    # Update user
    if status == 201:
        user_id = new_user['id']
        status, updated_user = client.update_user(user_id, email="charlie.updated@example.com")
        print_response("Update User", status, updated_user)
    
    # Send message
    status, message = client.send_message("Hello from REST client!", "Charlie")
    print_response("Send Message", status, message)
    
    # Get messages
    status, messages = client.get_messages()
    print_response("Get Messages", status, messages)
    
    # Delete user
    if 'user_id' in locals():
        status, result = client.delete_user(user_id)
        print_response("Delete User", status, result)
    
    print("\n🎉 REST API Demo completed!")

def interactive_mode():
    """Interactive mode for testing API"""
    client = RESTClient()
    
    print("\nInteractive REST Client Mode")
    print("Available commands:")
    print("1. health - Check server health")
    print("2. users - List all users")
    print("3. user <id> - Get specific user")
    print("4. create <name> <email> - Create user")
    print("5. update <id> <name> <email> - Update user")
    print("6. delete <id> - Delete user")
    print("7. messages - List messages")
    print("8. message <content> [sender] - Send message")
    print("9. exit - Exit interactive mode")
    
    while True:
        try:
            command = input("\n> ").strip().split()
            if not command:
                continue
                
            cmd = command[0].lower()
            
            if cmd == 'exit':
                break
            elif cmd == 'health':
                is_healthy, data = client.health_check()
                print(f"Status: {'Healthy' if is_healthy else 'Unhealthy'}")
                print(json.dumps(data, indent=2))
            elif cmd == 'users':
                status, data = client.get_users()
                print(f"Status: {status}")
                print(json.dumps(data, indent=2))
            elif cmd == 'user' and len(command) > 1:
                user_id = int(command[1])
                status, data = client.get_user(user_id)
                print(f"Status: {status}")
                print(json.dumps(data, indent=2))
            elif cmd == 'create' and len(command) > 2:
                name, email = command[1], command[2]
                status, data = client.create_user(name, email)
                print(f"Status: {status}")
                print(json.dumps(data, indent=2))
            elif cmd == 'messages':
                status, data = client.get_messages()
                print(f"Status: {status}")
                print(json.dumps(data, indent=2))
            elif cmd == 'message' and len(command) > 1:
                content = ' '.join(command[1:])
                sender = command[-1] if len(command) > 2 else None
                status, data = client.send_message(content, sender)
                print(f"Status: {status}")
                print(json.dumps(data, indent=2))
            else:
                print("Invalid command. Type 'exit' to quit.")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("Goodbye!")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        interactive_mode()
    else:
        demo_rest_api()