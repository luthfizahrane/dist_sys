#!/usr/bin/env python3
"""
TCP Socket Server Example
Implementasi server TCP socket untuk komunikasi low-level
"""

import socket
import threading
import json
import time
from datetime import datetime
import struct

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

class TCPClientHandler:
    """Handle individual TCP client connections"""
    
    def __init__(self, client_socket, client_address, server):
        self.client_socket = client_socket
        self.client_address = client_address
        self.server = server
        self.client_id = f"{client_address[0]}:{client_address[1]}"
        self.running = True
        self.buffer = b''
        
    def start(self):
        """Start handling client"""
        print(f"✅ Client connected: {self.client_id}")
        
        # Send welcome message
        welcome = {
            "type": "welcome",
            "client_id": self.client_id,
            "message": "Welcome to TCP Server!",
            "timestamp": datetime.now().isoformat()
        }
        self.send_message(welcome)
        
        # Start receiving messages
        thread = threading.Thread(target=self._handle_client)
        thread.daemon = True
        thread.start()
        
    def _handle_client(self):
        """Handle client messages"""
        try:
            while self.running:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                
                self.buffer += data
                
                # Process complete messages
                while True:
                    message, self.buffer = TCPProtocol.decode_message(self.buffer)
                    if message is None:
                        break
                    
                    self._process_message(message)
                    
        except ConnectionResetError:
            print(f"❌ Client {self.client_id} disconnected abruptly")
        except Exception as e:
            print(f"❌ Error handling client {self.client_id}: {e}")
        finally:
            self._cleanup()
    
    def _process_message(self, message):
        """Process received message"""
        print(f"📥 From {self.client_id}: {message}")
        
        if isinstance(message, dict):
            msg_type = message.get('type', 'unknown')
            
            if msg_type == 'ping':
                self._handle_ping(message)
            elif msg_type == 'echo':
                self._handle_echo(message)
            elif msg_type == 'broadcast':
                self._handle_broadcast(message)
            elif msg_type == 'get_stats':
                self._handle_get_stats()
            else:
                # Default echo behavior
                response = {
                    "type": "response",
                    "original_message": message,
                    "timestamp": datetime.now().isoformat(),
                    "from_server": True
                }
                self.send_message(response)
        else:
            # Handle plain text messages
            response = {
                "type": "echo",
                "original_text": message,
                "timestamp": datetime.now().isoformat(),
                "from_server": True
            }
            self.send_message(response)
    
    def _handle_ping(self, message):
        """Handle ping message"""
        pong = {
            "type": "pong",
            "ping_timestamp": message.get('timestamp'),
            "pong_timestamp": datetime.now().isoformat(),
            "client_id": self.client_id
        }
        self.send_message(pong)
    
    def _handle_echo(self, message):
        """Handle echo message"""
        echo_response = {
            "type": "echo_response",
            "content": message.get('content', ''),
            "timestamp": datetime.now().isoformat(),
            "echoed_by": "TCP Server"
        }
        self.send_message(echo_response)
    
    def _handle_broadcast(self, message):
        """Handle broadcast message"""
        broadcast_msg = {
            "type": "broadcast",
            "from_client": self.client_id,
            "content": message.get('content', ''),
            "timestamp": datetime.now().isoformat()
        }
        
        # Broadcast to all clients
        self.server.broadcast_message(broadcast_msg, exclude_client=self.client_id)
        
        # Send confirmation to sender
        confirmation = {
            "type": "broadcast_sent",
            "recipients": len(self.server.clients) - 1,
            "timestamp": datetime.now().isoformat()
        }
        self.send_message(confirmation)
    
    def _handle_get_stats(self):
        """Handle stats request"""
        stats = self.server.get_stats()
        self.send_message(stats)
    
    def send_message(self, message):
        """Send message to client"""
        try:
            encoded = TCPProtocol.encode_message(message)
            self.client_socket.send(encoded)
            print(f"📤 To {self.client_id}: {message}")
        except Exception as e:
            print(f"❌ Error sending to {self.client_id}: {e}")
            self._cleanup()
    
    def _cleanup(self):
        """Clean up client connection"""
        self.running = False
        try:
            self.client_socket.close()
        except:
            pass
        
        # Remove from server's client list
        if self.client_id in self.server.clients:
            del self.server.clients[self.client_id]
        
        print(f"🔌 Client {self.client_id} disconnected")

class TCPServer:
    """TCP Socket Server"""
    
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.clients = {}
        self.start_time = datetime.now()
        self.message_count = 0
        
    def start(self):
        """Start the TCP server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.running = True
            
            print(f"🚀 TCP Server started on {self.host}:{self.port}")
            print("Features:")
            print("- Custom binary protocol with length prefixes")
            print("- Multi-client support with threading")
            print("- Ping/Pong heartbeat")
            print("- Broadcast messaging")
            print("- Server statistics")
            print("- Message echoing")
            
            self._accept_connections()
            
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
    
    def _accept_connections(self):
        """Accept incoming connections"""
        print(f"\n🔵 Listening for connections on {self.host}:{self.port}...")
        
        try:
            while self.running:
                client_socket, client_address = self.server_socket.accept()
                
                # Create client handler
                client_handler = TCPClientHandler(client_socket, client_address, self)
                client_id = client_handler.client_id
                
                # Store client handler
                self.clients[client_id] = client_handler
                
                # Start handling client
                client_handler.start()
                
        except Exception as e:
            if self.running:
                print(f"❌ Error accepting connections: {e}")
    
    def broadcast_message(self, message, exclude_client=None):
        """Broadcast message to all clients"""
        for client_id, client_handler in self.clients.items():
            if client_id != exclude_client:
                client_handler.send_message(message)
        
        self.message_count += len(self.clients)
        if exclude_client:
            self.message_count -= 1
    
    def get_stats(self):
        """Get server statistics"""
        uptime = datetime.now() - self.start_time
        
        return {
            "type": "server_stats",
            "connected_clients": len(self.clients),
            "uptime_seconds": int(uptime.total_seconds()),
            "total_messages": self.message_count,
            "server_start_time": self.start_time.isoformat(),
            "current_time": datetime.now().isoformat()
        }
    
    def stop(self):
        """Stop the server"""
        print("\n🔴 Shutting down TCP Server...")
        self.running = False
        
        # Close all client connections
        for client_handler in list(self.clients.values()):
            client_handler._cleanup()
        
        # Close server socket
        if self.server_socket:
            self.server_socket.close()
        
        print("🛑 TCP Server stopped")

def main():
    """Main server function"""
    server = TCPServer()
    
    try:
        server.start()
        
    except KeyboardInterrupt:
        server.stop()
        print("Server stopped gracefully.")

if __name__ == '__main__':
    main()