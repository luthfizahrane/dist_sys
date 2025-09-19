#!/usr/bin/env python3
"""
TCP Socket Client Example
Implementasi client TCP socket untuk komunikasi low-level
"""

import socket
import json
import threading
import time
import struct
from datetime import datetime

class TCPProtocol:
    """Simple protocol for TCP communication"""
    
    @staticmethod
    def encode_message(message):
        """Encode message with length prefix"""
        if isinstance(message, dict):
            message = json.dumps(message)
        
        message_bytes = message.encode('utf-8')
        length = len(message_bytes)
        
        # Pack length as 4-byte big-endian integer
        length_prefix = struct.pack('>I', length)
        return length_prefix + message_bytes
    
    @staticmethod
    def decode_message(data):
        """Decode message with length prefix"""
        if len(data) < 4:
            return None, data
        
        # Unpack length from first 4 bytes
        length = struct.unpack('>I', data[:4])[0]
        
        if len(data) < 4 + length:
            return None, data  # Not enough data yet
        
        message_bytes = data[4:4+length]
        remaining_data = data[4+length:]
        
        try:
            message = json.loads(message_bytes.decode('utf-8'))
            return message, remaining_data
        except json.JSONDecodeError:
            return message_bytes.decode('utf-8'), remaining_data

class TCPClient:
    """TCP Socket Client"""
    
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.receive_thread = None
        self.buffer = b''
        self.message_callback = None
        
    def connect(self):
        """Connect to TCP server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            
            print(f"✅ Connected to TCP server at {self.host}:{self.port}")
            
            # Start receiving messages
            self.receive_thread = threading.Thread(target=self._receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from server"""
        self.connected = False
        
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        
        if self.receive_thread:
            self.receive_thread.join(timeout=1)
        
        print(f"🔌 Disconnected from {self.host}:{self.port}")
    
    def _receive_messages(self):
        """Background thread for receiving messages"""
        try:
            while self.connected:
                data = self.socket.recv(4096)
                if not data:
                    break
                
                self.buffer += data
                
                # Process complete messages
                while True:
                    message, self.buffer = TCPProtocol.decode_message(self.buffer)
                    if message is None:
                        break
                    
                    self._handle_received_message(message)
                    
        except ConnectionResetError:
            print("❌ Server disconnected")
        except Exception as e:
            if self.connected:
                print(f"❌ Error receiving messages: {e}")
        finally:
            self.connected = False
    
    def _handle_received_message(self, message):
        """Handle received message"""
        print(f"📥 Received: {json.dumps(message, indent=2) if isinstance(message, dict) else message}")
        
        if self.message_callback:
            self.message_callback(message)
    
    def send_message(self, message):
        """Send message to server"""
        if not self.connected:
            print("❌ Not connected to server")
            return False
        
        try:
            encoded = TCPProtocol.encode_message(message)
            self.socket.send(encoded)
            print(f"📤 Sent: {message}")
            return True
        except Exception as e:
            print(f"❌ Send failed: {e}")
            return False
    
    def set_message_callback(self, callback):
        """Set callback for received messages"""
        self.message_callback = callback
    
    def ping(self):
        """Send ping to server"""
        ping_msg = {
            "type": "ping",
            "timestamp": datetime.now().isoformat(),
            "client_info": f"TCP Client {self.host}:{self.port}"
        }
        return self.send_message(ping_msg)
    
    def echo(self, content):
        """Send echo message"""
        echo_msg = {
            "type": "echo",
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        return self.send_message(echo_msg)
    
    def broadcast(self, content):
        """Send broadcast message"""
        broadcast_msg = {
            "type": "broadcast",
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        return self.send_message(broadcast_msg)
    
    def get_server_stats(self):
        """Request server statistics"""
        stats_msg = {
            "type": "get_stats",
            "timestamp": datetime.now().isoformat()
        }
        return self.send_message(stats_msg)
    
    def send_custom_message(self, msg_type, data=None):
        """Send custom message"""
        message = {
            "type": msg_type,
            "timestamp": datetime.now().isoformat()
        }
        
        if data:
            message.update(data)
        
        return self.send_message(message)

def demo_tcp_client():
    """Demonstrate TCP client functionality"""
    print("TCP Socket Client Demo")
    print("=====================")
    
    client = TCPClient()
    
    # Set message callback
    def on_message(message):
        if isinstance(message, dict):
            msg_type = message.get('type', 'unknown')
            if msg_type == 'pong':
                ping_time = message.get('ping_timestamp', '')
                pong_time = message.get('pong_timestamp', '')
                print(f"🏓 Ping-Pong completed: {ping_time} -> {pong_time}")
            elif msg_type == 'echo_response':
                print(f"🔄 Echo: {message.get('content', '')}")
            elif msg_type == 'broadcast':
                print(f"📢 Broadcast from {message.get('from_client', 'unknown')}: {message.get('content', '')}")
            elif msg_type == 'server_stats':
                print(f"📊 Server Stats:")
                print(f"   Connected clients: {message.get('connected_clients', 0)}")
                print(f"   Uptime: {message.get('uptime_seconds', 0)} seconds")
                print(f"   Total messages: {message.get('total_messages', 0)}")
    
    client.set_message_callback(on_message)
    
    if not client.connect():
        print("❌ Cannot connect to server. Please start the server first:")
        print("   python server.py")
        return
    
    try:
        # Wait for welcome message
        time.sleep(1)
        
        print("\n🔵 Testing Ping/Pong")
        client.ping()
        time.sleep(1)
        
        print("\n🟢 Testing Echo Messages")
        client.echo("Hello TCP Server!")
        time.sleep(1)
        
        client.echo("This is a test message for echo")
        time.sleep(1)
        
        print("\n🟡 Testing Broadcast Messages")
        client.broadcast("Hello all clients!")
        time.sleep(1)
        
        print("\n🔴 Testing Server Statistics")
        client.get_server_stats()
        time.sleep(1)
        
        print("\n🟣 Testing Custom Messages")
        client.send_custom_message("custom_test", {
            "data": "custom payload",
            "test_id": 123
        })
        time.sleep(1)
        
        print("\n🟠 Testing Plain Text Message")
        client.send_message("This is a plain text message")
        time.sleep(1)
        
        print("\n🎉 TCP demo completed!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
    
    finally:
        time.sleep(2)  # Wait for any pending messages
        client.disconnect()

def interactive_mode():
    """Interactive mode for TCP client"""
    client = TCPClient()
    
    def on_message(message):
        if isinstance(message, dict):
            msg_type = message.get('type', 'unknown')
            if msg_type == 'welcome':
                print(f"\n✅ {message.get('message', 'Connected')}")
            elif msg_type == 'broadcast':
                from_client = message.get('from_client', 'unknown')
                content = message.get('content', '')
                print(f"\n📢 Broadcast from {from_client}: {content}")
            else:
                print(f"\n📥 Server response: {message}")
        else:
            print(f"\n📥 Server: {message}")
        print("TCP> ", end="", flush=True)
    
    client.set_message_callback(on_message)
    
    if not client.connect():
        print("❌ Cannot connect to server")
        return
    
    print(f"\n🔧 Interactive TCP Client Mode")
    print("Commands:")
    print("  /ping - Send ping to server")
    print("  /echo <message> - Send echo message")
    print("  /broadcast <message> - Send broadcast message")
    print("  /stats - Get server statistics")
    print("  /custom <type> - Send custom message")
    print("  /exit - Exit interactive mode")
    print("  Just type to send plain text messages")
    print("\nStarting TCP session...")
    
    try:
        time.sleep(1)  # Wait for welcome message
        
        while True:
            message = input("TCP> ").strip()
            
            if not message:
                continue
            elif message == '/exit':
                break
            elif message == '/ping':
                client.ping()
            elif message.startswith('/echo '):
                content = message[6:]  # Remove '/echo '
                client.echo(content)
            elif message.startswith('/broadcast '):
                content = message[11:]  # Remove '/broadcast '
                client.broadcast(content)
            elif message == '/stats':
                client.get_server_stats()
            elif message.startswith('/custom '):
                msg_type = message[8:]  # Remove '/custom '
                client.send_custom_message(msg_type, {"interactive": True})
            else:
                client.send_message(message)
            
            time.sleep(0.1)  # Small delay for responses
                
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        client.disconnect()
        print("\n👋 TCP session ended!")

def performance_test():
    """Performance test for TCP client"""
    print("TCP Performance Test")
    print("==================")
    
    client = TCPClient()
    
    message_count = 0
    response_count = 0
    
    def on_message(message):
        nonlocal response_count
        response_count += 1
    
    client.set_message_callback(on_message)
    
    if not client.connect():
        print("❌ Cannot connect to server")
        return
    
    print("🚀 Sending 100 messages rapidly...")
    
    start_time = time.time()
    
    # Send 100 echo messages
    for i in range(100):
        client.echo(f"Performance test message {i+1}")
        message_count += 1
        time.sleep(0.01)  # 10ms between messages
    
    # Wait for responses
    print("⏳ Waiting for responses...")
    time.sleep(5)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✅ Performance test completed!")
    print(f"   Messages sent: {message_count}")
    print(f"   Responses received: {response_count}")
    print(f"   Duration: {duration:.2f} seconds")
    print(f"   Messages per second: {message_count/duration:.2f}")
    print(f"   Round-trip success rate: {(response_count/message_count)*100:.1f}%")
    
    client.disconnect()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == 'interactive':
            interactive_mode()
        elif mode == 'performance':
            performance_test()
        else:
            print("Available modes: interactive, performance")
    else:
        demo_tcp_client()