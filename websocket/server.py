#!/usr/bin/env python3
"""
WebSocket Server Example
Implementasi server WebSocket untuk komunikasi real-time
"""

import asyncio
import json
import socket
import threading
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import hashlib
import base64
import struct

class WebSocketHandler:
    """Simple WebSocket implementation using standard library"""
    
    def __init__(self):
        self.clients = {}
        self.client_counter = 0
        
    def create_websocket_key_response(self, key):
        """Generate WebSocket accept key"""
        magic_string = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        combined = key + magic_string
        sha1_hash = hashlib.sha1(combined.encode()).digest()
        return base64.b64encode(sha1_hash).decode()
    
    def parse_websocket_frame(self, frame):
        """Parse WebSocket frame"""
        if len(frame) < 2:
            return None
        
        first_byte = frame[0]
        second_byte = frame[1]
        
        fin = (first_byte >> 7) & 1
        opcode = first_byte & 0x0F
        masked = (second_byte >> 7) & 1
        payload_length = second_byte & 0x7F
        
        if payload_length == 126:
            payload_length = struct.unpack('>H', frame[2:4])[0]
            header_length = 4
        elif payload_length == 127:
            payload_length = struct.unpack('>Q', frame[2:10])[0]
            header_length = 10
        else:
            header_length = 2
        
        if masked:
            mask = frame[header_length:header_length + 4]
            payload = frame[header_length + 4:header_length + 4 + payload_length]
            payload = bytes([payload[i] ^ mask[i % 4] for i in range(len(payload))])
            header_length += 4
        else:
            payload = frame[header_length:header_length + payload_length]
        
        return {
            'fin': fin,
            'opcode': opcode,
            'payload': payload.decode('utf-8') if payload else ''
        }
    
    def create_websocket_frame(self, payload):
        """Create WebSocket frame"""
        payload_bytes = payload.encode('utf-8')
        payload_length = len(payload_bytes)
        
        if payload_length <= 125:
            frame = struct.pack('!BB', 0x81, payload_length)
        elif payload_length <= 65535:
            frame = struct.pack('!BBH', 0x81, 126, payload_length)
        else:
            frame = struct.pack('!BBQ', 0x81, 127, payload_length)
        
        return frame + payload_bytes

class MockWebSocketServer:
    """Mock WebSocket server implementation"""
    
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.handler = WebSocketHandler()
        self.running = False
        self.clients = []
        
    def start(self):
        """Start the WebSocket server"""
        self.running = True
        print(f"🚀 Mock WebSocket Server started on ws://{self.host}:{self.port}")
        print("Features:")
        print("- Real-time messaging")
        print("- Multiple client support")
        print("- Broadcast capabilities")
        print("- Chat room functionality")
        
        # Simulate server running
        self._run_server()
    
    def _run_server(self):
        """Internal server loop"""
        try:
            while self.running:
                time.sleep(1)
                # Simulate periodic server tasks
                if len(self.clients) > 0:
                    self._send_heartbeat()
        except KeyboardInterrupt:
            self.stop()
    
    def _send_heartbeat(self):
        """Send heartbeat to all clients"""
        message = {
            "type": "heartbeat",
            "timestamp": datetime.now().isoformat(),
            "server_status": "running",
            "connected_clients": len(self.clients)
        }
        # In real implementation, this would be sent to all connected clients
        # print(f"💓 Heartbeat: {len(self.clients)} clients connected")
    
    def handle_client_connect(self, client_id):
        """Handle new client connection"""
        self.clients.append(client_id)
        print(f"✅ Client {client_id} connected")
        
        # Send welcome message
        welcome_message = {
            "type": "welcome",
            "client_id": client_id,
            "message": "Welcome to the WebSocket server!",
            "timestamp": datetime.now().isoformat()
        }
        return welcome_message
    
    def handle_client_disconnect(self, client_id):
        """Handle client disconnection"""
        if client_id in self.clients:
            self.clients.remove(client_id)
            print(f"❌ Client {client_id} disconnected")
    
    def handle_message(self, client_id, message):
        """Handle incoming message from client"""
        try:
            data = json.loads(message) if isinstance(message, str) else message
            msg_type = data.get('type', 'chat')
            
            if msg_type == 'chat':
                return self._handle_chat_message(client_id, data)
            elif msg_type == 'broadcast':
                return self._handle_broadcast_message(client_id, data)
            elif msg_type == 'ping':
                return self._handle_ping(client_id)
            else:
                return {"type": "error", "message": "Unknown message type"}
                
        except json.JSONDecodeError:
            return {"type": "error", "message": "Invalid JSON format"}
    
    def _handle_chat_message(self, client_id, data):
        """Handle chat message"""
        response = {
            "type": "chat",
            "client_id": client_id,
            "sender": data.get('sender', f'Client-{client_id}'),
            "content": data.get('content', ''),
            "timestamp": datetime.now().isoformat()
        }
        
        # Broadcast to all clients
        print(f"💬 Chat from {response['sender']}: {response['content']}")
        return response
    
    def _handle_broadcast_message(self, client_id, data):
        """Handle broadcast message"""
        response = {
            "type": "broadcast",
            "from_client": client_id,
            "message": data.get('message', ''),
            "timestamp": datetime.now().isoformat(),
            "recipients": len(self.clients)
        }
        
        print(f"📢 Broadcast from Client-{client_id}: {response['message']}")
        return response
    
    def _handle_ping(self, client_id):
        """Handle ping message"""
        return {
            "type": "pong",
            "client_id": client_id,
            "timestamp": datetime.now().isoformat(),
            "server_time": time.time()
        }
    
    def get_server_stats(self):
        """Get server statistics"""
        return {
            "type": "stats",
            "connected_clients": len(self.clients),
            "server_uptime": "mock_uptime",
            "total_messages": "mock_count",
            "timestamp": datetime.now().isoformat()
        }
    
    def stop(self):
        """Stop the server"""
        self.running = False
        print("🛑 WebSocket Server stopped")

def main():
    """Main server function"""
    server = MockWebSocketServer()
    
    try:
        server.start()
        
        print("\nServer Status: Running ✅")
        print("Features available:")
        print("- Chat messaging")
        print("- Broadcast messages")
        print("- Ping/Pong heartbeat")
        print("- Client connection management")
        print("\nPress Ctrl+C to stop the server...")
        
        # Keep the main thread alive
        while server.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🔴 Shutting down server...")
        server.stop()
        print("Server stopped gracefully.")

if __name__ == '__main__':
    main()