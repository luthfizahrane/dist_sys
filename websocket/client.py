#!/usr/bin/env python3
"""
WebSocket Client Example
Implementasi client WebSocket untuk komunikasi real-time
"""

import json
import time
import threading
from datetime import datetime
import random

class MockWebSocketClient:
    """Mock WebSocket client implementation"""
    
    def __init__(self, uri="ws://localhost:8765", client_id=None):
        self.uri = uri
        self.client_id = client_id or f"client-{random.randint(1000, 9999)}"
        self.connected = False
        self.message_callback = None
        self.receive_thread = None
        self.message_queue = []
        
    def connect(self):
        """Connect to WebSocket server"""
        try:
            # Simulate WebSocket connection
            self.connected = True
            print(f"✅ Connected to {self.uri} as {self.client_id}")
            
            # Start receiving messages in background
            self.receive_thread = threading.Thread(target=self._receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            # Simulate server welcome message
            welcome_msg = {
                "type": "welcome",
                "client_id": self.client_id,
                "message": "Welcome to the WebSocket server!",
                "timestamp": datetime.now().isoformat()
            }
            self._handle_received_message(welcome_msg)
            
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from server"""
        self.connected = False
        if self.receive_thread:
            self.receive_thread.join(timeout=1)
        print(f"🔌 Disconnected from {self.uri}")
    
    def send_message(self, message):
        """Send message to server"""
        if not self.connected:
            print("❌ Not connected to server")
            return False
        
        try:
            # Simulate sending message and getting response
            if isinstance(message, dict):
                message_str = json.dumps(message)
            else:
                message_str = str(message)
            
            print(f"📤 Sending: {message_str}")
            
            # Simulate server response
            response = self._simulate_server_response(message)
            self.message_queue.append(response)
            
            return True
        except Exception as e:
            print(f"❌ Send failed: {e}")
            return False
    
    def _simulate_server_response(self, message):
        """Simulate server response to client message"""
        if isinstance(message, str):
            try:
                message = json.loads(message)
            except json.JSONDecodeError:
                message = {"type": "chat", "content": message}
        
        msg_type = message.get('type', 'chat')
        
        if msg_type == 'chat':
            return {
                "type": "chat",
                "client_id": self.client_id,
                "sender": message.get('sender', self.client_id),
                "content": message.get('content', ''),
                "timestamp": datetime.now().isoformat(),
                "echo": True
            }
        elif msg_type == 'ping':
            return {
                "type": "pong",
                "client_id": self.client_id,
                "timestamp": datetime.now().isoformat(),
                "server_time": time.time()
            }
        elif msg_type == 'broadcast':
            return {
                "type": "broadcast_ack",
                "from_client": self.client_id,
                "message": message.get('message', ''),
                "timestamp": datetime.now().isoformat(),
                "recipients": random.randint(1, 5)
            }
        else:
            return {
                "type": "response",
                "original_type": msg_type,
                "timestamp": datetime.now().isoformat(),
                "status": "processed"
            }
    
    def _receive_messages(self):
        """Background thread for receiving messages"""
        while self.connected:
            if self.message_queue:
                message = self.message_queue.pop(0)
                self._handle_received_message(message)
            time.sleep(0.1)
    
    def _handle_received_message(self, message):
        """Handle received message"""
        print(f"📥 Received: {json.dumps(message, indent=2)}")
        
        if self.message_callback:
            self.message_callback(message)
    
    def set_message_callback(self, callback):
        """Set callback for received messages"""
        self.message_callback = callback
    
    def send_chat_message(self, content, sender=None):
        """Send chat message"""
        message = {
            "type": "chat",
            "sender": sender or self.client_id,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        return self.send_message(message)
    
    def send_broadcast(self, message):
        """Send broadcast message"""
        broadcast = {
            "type": "broadcast",
            "message": message,
            "from": self.client_id,
            "timestamp": datetime.now().isoformat()
        }
        return self.send_message(broadcast)
    
    def ping(self):
        """Send ping to server"""
        ping_msg = {
            "type": "ping",
            "client_id": self.client_id,
            "timestamp": datetime.now().isoformat()
        }
        return self.send_message(ping_msg)

def demo_websocket_client():
    """Demonstrate WebSocket client functionality"""
    print("WebSocket Client Demo")
    print("===================")
    
    client = MockWebSocketClient()
    
    # Set up message callback
    def on_message(message):
        msg_type = message.get('type', 'unknown')
        if msg_type == 'chat':
            print(f"💬 Chat from {message.get('sender')}: {message.get('content')}")
        elif msg_type == 'broadcast':
            print(f"📢 Broadcast: {message.get('message')}")
        elif msg_type == 'pong':
            print(f"🏓 Pong received at {message.get('timestamp')}")
    
    client.set_message_callback(on_message)
    
    if not client.connect():
        print("❌ Cannot connect to server. Please start the server first:")
        print("   python server.py")
        return
    
    try:
        print("\n🔵 Testing Chat Messages")
        
        # Send chat messages
        client.send_chat_message("Hello WebSocket server!")
        time.sleep(1)
        
        client.send_chat_message("This is a real-time message", "Demo Client")
        time.sleep(1)
        
        client.send_chat_message("WebSocket is great for real-time apps!")
        time.sleep(1)
        
        print("\n🟢 Testing Broadcast Messages")
        
        # Send broadcast
        client.send_broadcast("This is a broadcast message to all clients!")
        time.sleep(1)
        
        print("\n🟡 Testing Ping/Pong")
        
        # Send ping
        client.ping()
        time.sleep(1)
        
        print("\n🔴 Testing Custom Messages")
        
        # Send custom message
        custom_message = {
            "type": "custom",
            "action": "get_stats",
            "client_id": client.client_id
        }
        client.send_message(custom_message)
        time.sleep(1)
        
        print("\n🎉 WebSocket demo completed!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
    
    finally:
        time.sleep(2)  # Wait for any pending messages
        client.disconnect()

def chat_mode():
    """Interactive chat mode"""
    client = MockWebSocketClient()
    
    def on_message(message):
        msg_type = message.get('type')
        if msg_type == 'chat':
            sender = message.get('sender', 'Unknown')
            content = message.get('content', '')
            if not message.get('echo'):  # Don't show our own messages
                print(f"\n💬 {sender}: {content}")
                print("Chat> ", end="", flush=True)
        elif msg_type == 'broadcast':
            print(f"\n📢 Broadcast: {message.get('message')}")
            print("Chat> ", end="", flush=True)
    
    client.set_message_callback(on_message)
    
    if not client.connect():
        print("❌ Cannot connect to server")
        return
    
    print(f"\n💬 Chat Mode - Connected as {client.client_id}")
    print("Commands:")
    print("  /broadcast <message> - Send broadcast message")
    print("  /ping - Send ping to server")
    print("  /exit - Exit chat mode")
    print("  Just type to send chat messages")
    print("\nStarting chat...")
    
    try:
        while True:
            message = input("Chat> ").strip()
            
            if not message:
                continue
            elif message == '/exit':
                break
            elif message.startswith('/broadcast '):
                broadcast_msg = message[11:]  # Remove '/broadcast '
                client.send_broadcast(broadcast_msg)
            elif message == '/ping':
                client.ping()
            else:
                client.send_chat_message(message)
            
            time.sleep(0.1)  # Small delay to see responses
                
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        client.disconnect()
        print("\n👋 Chat session ended!")

def stress_test():
    """Stress test with multiple messages"""
    print("WebSocket Stress Test")
    print("====================")
    
    client = MockWebSocketClient()
    
    message_count = 0
    def on_message(message):
        nonlocal message_count
        message_count += 1
    
    client.set_message_callback(on_message)
    
    if not client.connect():
        print("❌ Cannot connect to server")
        return
    
    print("🚀 Sending 50 messages rapidly...")
    
    start_time = time.time()
    
    for i in range(50):
        client.send_chat_message(f"Stress test message {i+1}")
        time.sleep(0.05)  # 50ms between messages
    
    # Wait for responses
    time.sleep(3)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✅ Stress test completed!")
    print(f"   Messages sent: 50")
    print(f"   Responses received: {message_count}")
    print(f"   Duration: {duration:.2f} seconds")
    print(f"   Messages per second: {50/duration:.2f}")
    
    client.disconnect()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == 'chat':
            chat_mode()
        elif mode == 'stress':
            stress_test()
        else:
            print("Available modes: chat, stress")
    else:
        demo_websocket_client()