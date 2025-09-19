#!/usr/bin/env python3
"""
Redis Subscriber Example
Implementasi subscriber untuk Redis Pub/Sub messaging
"""

import json
import time
import threading
from datetime import datetime

class MockRedisSubscriber:
    """Mock Redis subscriber implementation"""
    
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.connected = False
        self.subscribed_channels = set()
        self.message_callback = None
        self.listening = False
        self.received_messages = []
        self.listen_thread = None
        
    def connect(self):
        """Connect to Redis server"""
        try:
            # Simulate Redis connection
            self.connected = True
            print(f"✅ Connected to Redis at {self.host}:{self.port}/{self.db}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from Redis"""
        self.connected = False
        self.listening = False
        
        if self.listen_thread:
            self.listen_thread.join(timeout=1)
        
        print("🔌 Disconnected from Redis")
    
    def subscribe(self, *channels):
        """Subscribe to one or more channels"""
        if not self.connected:
            print("❌ Not connected to Redis")
            return False
        
        for channel in channels:
            self.subscribed_channels.add(channel)
            print(f"📥 Subscribed to channel: '{channel}'")
        
        return True
    
    def unsubscribe(self, *channels):
        """Unsubscribe from channels"""
        if not channels:
            # Unsubscribe from all
            channels = list(self.subscribed_channels)
        
        for channel in channels:
            if channel in self.subscribed_channels:
                self.subscribed_channels.remove(channel)
                print(f"📤 Unsubscribed from channel: '{channel}'")
        
        return True
    
    def set_message_callback(self, callback):
        """Set callback function for received messages"""
        self.message_callback = callback
    
    def listen(self):
        """Start listening for messages"""
        if not self.connected:
            print("❌ Not connected to Redis")
            return
        
        if not self.subscribed_channels:
            print("❌ No channels subscribed")
            return
        
        self.listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop)
        self.listen_thread.daemon = True
        self.listen_thread.start()
        
        print(f"👂 Listening for messages on channels: {', '.join(self.subscribed_channels)}")
    
    def _listen_loop(self):
        """Internal listening loop"""
        try:
            while self.listening and self.connected:
                # Simulate receiving messages
                self._simulate_messages()
                time.sleep(1)  # Check for messages every second
                
        except Exception as e:
            print(f"❌ Error in listen loop: {e}")
        finally:
            self.listening = False
    
    def _simulate_messages(self):
        """Simulate receiving messages (for demo purposes)"""
        # In real implementation, this would receive actual Redis messages
        
        # Simulate occasional messages
        import random
        
        if random.random() < 0.3:  # 30% chance of receiving a message
            channel = random.choice(list(self.subscribed_channels))
            
            # Create a mock message
            mock_message = {
                'type': 'message',
                'channel': channel,
                'data': {
                    'simulated': True,
                    'content': f'Mock message for {channel}',
                    'timestamp': datetime.now().isoformat(),
                    'message_id': len(self.received_messages) + 1
                }
            }
            
            self._handle_message(mock_message)
    
    def _handle_message(self, message):
        """Handle received message"""
        self.received_messages.append(message)
        
        channel = message.get('channel', 'unknown')
        data = message.get('data', {})
        
        print(f"📨 Received on '{channel}': {json.dumps(data, indent=2)}")
        
        if self.message_callback:
            self.message_callback(message)
    
    def inject_message(self, channel, data):
        """Inject a message for testing purposes"""
        if channel in self.subscribed_channels:
            message = {
                'type': 'message',
                'channel': channel,
                'data': data
            }
            self._handle_message(message)
            return True
        return False
    
    def get_statistics(self):
        """Get subscriber statistics"""
        channel_counts = {}
        
        for msg in self.received_messages:
            channel = msg.get('channel', 'unknown')
            channel_counts[channel] = channel_counts.get(channel, 0) + 1
        
        return {
            'subscribed_channels': list(self.subscribed_channels),
            'total_messages_received': len(self.received_messages),
            'messages_per_channel': channel_counts,
            'listening': self.listening,
            'connection_status': 'connected' if self.connected else 'disconnected'
        }
    
    def stop_listening(self):
        """Stop listening for messages"""
        self.listening = False
        print("🛑 Stopped listening for messages")

def demo_redis_subscriber():
    """Demonstrate Redis subscriber functionality"""
    print("Redis Subscriber Demo")
    print("===================")
    
    subscriber = MockRedisSubscriber()
    
    # Set up message callback
    def on_message(message):
        channel = message.get('channel', 'unknown')
        data = message.get('data', {})
        msg_type = data.get('type', 'unknown')
        
        if msg_type == 'chat':
            user = data.get('user', 'unknown')
            content = data.get('message', '')
            print(f"💬 Chat from {user}: {content}")
        elif msg_type == 'alert':
            level = data.get('level', 'info')
            msg = data.get('message', '')
            print(f"🚨 Alert [{level}]: {msg}")
        elif msg_type == 'event':
            event = data.get('event', 'unknown')
            print(f"📅 Event: {event}")
    
    subscriber.set_message_callback(on_message)
    
    if not subscriber.connect():
        print("❌ Cannot connect to Redis. Please start Redis server:")
        print("   docker run -d -p 6379:6379 redis:alpine")
        return
    
    try:
        print("\n🔵 Subscribing to Channels")
        
        # Subscribe to multiple channels
        subscriber.subscribe('news', 'alerts', 'chat', 'events')
        
        print("\n🟢 Starting Message Listener")
        
        # Start listening
        subscriber.listen()
        
        print("\n🟡 Injecting Test Messages")
        
        # Inject some test messages to demonstrate functionality
        test_messages = [
            ('news', {'type': 'news', 'title': 'Breaking News', 'content': 'Redis Pub/Sub working!'}),
            ('alerts', {'type': 'alert', 'level': 'warning', 'message': 'High CPU usage detected'}),
            ('chat', {'type': 'chat', 'user': 'demo_user', 'message': 'Hello subscribers!'}),
            ('events', {'type': 'event', 'event': 'user_login', 'user_id': 123}),
            ('news', {'type': 'news', 'title': 'Update', 'content': 'System update completed'}),
        ]
        
        for channel, data in test_messages:
            time.sleep(1)
            subscriber.inject_message(channel, data)
        
        print("\n🔴 Waiting for Messages (10 seconds)")
        time.sleep(10)
        
        print("\n🟣 Subscriber Statistics")
        
        stats = subscriber.get_statistics()
        print(f"📊 Subscriber Statistics:")
        print(f"   Subscribed channels: {', '.join(stats['subscribed_channels'])}")
        print(f"   Total messages received: {stats['total_messages_received']}")
        print(f"   Listening: {stats['listening']}")
        print(f"   Connection status: {stats['connection_status']}")
        print(f"   Messages per channel:")
        for channel, count in stats['messages_per_channel'].items():
            print(f"     {channel}: {count}")
        
        print("\n🎉 Redis Subscriber demo completed!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
    
    finally:
        subscriber.stop_listening()
        subscriber.disconnect()

def interactive_subscriber():
    """Interactive Redis subscriber"""
    subscriber = MockRedisSubscriber()
    
    def on_message(message):
        channel = message.get('channel', 'unknown')
        data = message.get('data', {})
        print(f"\n📨 [{channel}] {json.dumps(data, indent=2)}")
        print("Subscriber> ", end="", flush=True)
    
    subscriber.set_message_callback(on_message)
    
    if not subscriber.connect():
        print("❌ Cannot connect to Redis")
        return
    
    print(f"\n📥 Interactive Redis Subscriber")
    print("Commands:")
    print("  sub <channel1> [channel2] ... - Subscribe to channels")
    print("  unsub <channel1> [channel2] ... - Unsubscribe from channels")
    print("  listen - Start listening for messages")
    print("  stop - Stop listening")
    print("  inject <channel> <message> - Inject test message")
    print("  stats - Show subscriber statistics")
    print("  exit - Exit subscriber mode")
    
    try:
        while True:
            command = input("\nSubscriber> ").strip().split()
            
            if not command:
                continue
            
            cmd = command[0].lower()
            
            if cmd == 'exit':
                break
            elif cmd == 'sub' and len(command) > 1:
                channels = command[1:]
                subscriber.subscribe(*channels)
                
            elif cmd == 'unsub':
                channels = command[1:] if len(command) > 1 else []
                subscriber.unsubscribe(*channels)
                
            elif cmd == 'listen':
                if subscriber.subscribed_channels:
                    subscriber.listen()
                else:
                    print("❌ No channels subscribed")
                    
            elif cmd == 'stop':
                subscriber.stop_listening()
                
            elif cmd == 'inject' and len(command) >= 3:
                channel = command[1]
                message_str = ' '.join(command[2:])
                
                try:
                    # Try to parse as JSON
                    message_data = json.loads(message_str)
                except json.JSONDecodeError:
                    # Use as string
                    message_data = {'content': message_str}
                
                if subscriber.inject_message(channel, message_data):
                    print(f"✅ Injected message to '{channel}'")
                else:
                    print(f"❌ Not subscribed to '{channel}'")
                    
            elif cmd == 'stats':
                stats = subscriber.get_statistics()
                print(json.dumps(stats, indent=2))
                
            else:
                print("❌ Invalid command")
                
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        subscriber.stop_listening()
        subscriber.disconnect()
        print("\n👋 Subscriber session ended!")

def channel_monitor():
    """Monitor specific channels"""
    print("Redis Channel Monitor")
    print("===================")
    
    subscriber = MockRedisSubscriber()
    
    message_counts = {}
    
    def on_message(message):
        channel = message.get('channel', 'unknown')
        data = message.get('data', {})
        
        # Count messages
        message_counts[channel] = message_counts.get(channel, 0) + 1
        
        # Display message with channel info
        timestamp = data.get('timestamp', datetime.now().isoformat())
        content = data.get('content', str(data))
        
        print(f"[{timestamp}] {channel}: {content}")
        print(f"   Total messages from {channel}: {message_counts[channel]}")
    
    subscriber.set_message_callback(on_message)
    
    if not subscriber.connect():
        print("❌ Cannot connect to Redis")
        return
    
    # Subscribe to monitoring channels
    channels = ['logs', 'metrics', 'alerts', 'events']
    subscriber.subscribe(*channels)
    subscriber.listen()
    
    print(f"📊 Monitoring channels: {', '.join(channels)}")
    print("Generating test traffic...")
    
    try:
        # Generate test messages
        for i in range(20):
            import random
            
            channel = random.choice(channels)
            test_data = {
                'id': i + 1,
                'content': f'Test message {i + 1} for {channel}',
                'timestamp': datetime.now().isoformat(),
                'priority': random.choice(['low', 'medium', 'high'])
            }
            
            subscriber.inject_message(channel, test_data)
            time.sleep(0.5)
        
        print("\n📈 Final Statistics:")
        for channel, count in message_counts.items():
            print(f"   {channel}: {count} messages")
        
    except KeyboardInterrupt:
        pass
    
    finally:
        subscriber.stop_listening()
        subscriber.disconnect()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == 'interactive':
            interactive_subscriber()
        elif mode == 'monitor':
            channel_monitor()
        else:
            print("Available modes: interactive, monitor")
    else:
        demo_redis_subscriber()