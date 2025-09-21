#!/usr/bin/env python3
"""
Redis Publisher Example
Implementasi publisher untuk Redis Pub/Sub messaging
"""

import json
import time
from datetime import datetime
import threading

class MockRedisPublisher:
    """Mock Redis publisher implementation"""
    
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.connected = False
        self.published_messages = []
        
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
        print("🔌 Disconnected from Redis")
    
    def publish(self, channel, message):
        """Publish message to channel"""
        if not self.connected:
            print("❌ Not connected to Redis")
            return False
        
        try:
            # Prepare message
            if isinstance(message, dict):
                message_data = message.copy()
                message_data['published_at'] = datetime.now().isoformat()
                message_str = json.dumps(message_data)
            else:
                message_str = str(message)
            
            # Store published message (for mock purposes)
            published_msg = {
                'channel': channel,
                'message': message_str,
                'timestamp': datetime.now().isoformat()
            }
            self.published_messages.append(published_msg)
            
            print(f"📤 Published to '{channel}': {message_str}")
            
            # Simulate Redis publish response (number of subscribers)
            subscribers = self._simulate_subscriber_count(channel)
            print(f"   📊 Message delivered to {subscribers} subscribers")
            
            return True
            
        except Exception as e:
            print(f"❌ Publish failed: {e}")
            return False
    
    def _simulate_subscriber_count(self, channel):
        """Simulate number of subscribers for a channel"""
        # Different channels have different subscriber counts
        channel_subscribers = {
            'news': 5,
            'alerts': 3,
            'chat': 8,
            'logs': 2,
            'events': 4
        }
        return channel_subscribers.get(channel, 1)
    
    def publish_multiple(self, messages):
        """Publish multiple messages"""
        published_count = 0
        
        for channel, message in messages:
            if self.publish(channel, message):
                published_count += 1
            time.sleep(0.1)  # Small delay between messages
        
        return published_count
    
    def publish_periodic(self, channel, message_template, interval=1, count=10):
        """Publish messages periodically"""
        print(f"🔄 Starting periodic publishing to '{channel}' (interval: {interval}s, count: {count})")
        
        for i in range(count):
            message = {
                "template": message_template,
                "sequence": i + 1,
                "total": count,
                "timestamp": datetime.now().isoformat()
            }
            
            self.publish(channel, message)
            
            if i < count - 1:  # Don't sleep after last message
                time.sleep(interval)
        
        print(f"✅ Periodic publishing completed")
    
    def get_statistics(self):
        """Get publisher statistics"""
        channel_counts = {}
        
        for msg in self.published_messages:
            channel = msg['channel']
            channel_counts[channel] = channel_counts.get(channel, 0) + 1
        
        return {
            'total_messages': len(self.published_messages),
            'unique_channels': len(channel_counts),
            'messages_per_channel': channel_counts,
            'connection_status': 'connected' if self.connected else 'disconnected'
        }

def demo_redis_publisher():
    """Demonstrate Redis publisher functionality"""
    print("Redis Publisher Demo")
    print("==================")
    
    publisher = MockRedisPublisher()
    
    if not publisher.connect():
        print("❌ Cannot connect to Redis. Please start Redis server:")
        print("   docker run -d -p 6379:6379 redis:alpine")
        return
    
    try:
        print("\n🔵 Publishing Single Messages")
        
        # Publish to different channels
        publisher.publish('news', {
            'title': 'Breaking News',
            'content': 'Redis Pub/Sub is working!',
            'priority': 'high'
        })
        
        publisher.publish('alerts', {
            'type': 'system',
            'message': 'Server status: OK',
            'level': 'info'
        })
        
        publisher.publish('chat', {
            'user': 'publisher_demo',
            'message': 'Hello from Redis publisher!',
            'room': 'general'
        })
        
        time.sleep(1)
        
        print("\n🟢 Publishing Multiple Messages")
        
        batch_messages = [
            ('events', {'event': 'user_login', 'user_id': 123}),
            ('events', {'event': 'user_logout', 'user_id': 123}),
            ('logs', {'level': 'info', 'message': 'Application started'}),
            ('logs', {'level': 'debug', 'message': 'Debug information'}),
        ]
        
        published_count = publisher.publish_multiple(batch_messages)
        print(f"   ✅ Published {published_count} messages")
        
        print("\n🟡 Periodic Publishing")
        
        publisher.publish_periodic(
            channel='heartbeat',
            message_template='Server heartbeat',
            interval=0.5,
            count=5
        )
        
        print("\n🔴 Publisher Statistics")
        
        stats = publisher.get_statistics()
        print(f"📊 Publisher Statistics:")
        print(f"   Total messages: {stats['total_messages']}")
        print(f"   Unique channels: {stats['unique_channels']}")
        print(f"   Connection status: {stats['connection_status']}")
        print(f"   Messages per channel:")
        for channel, count in stats['messages_per_channel'].items():
            print(f"     {channel}: {count}")
        
        print("\n🎉 Redis Publisher demo completed!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
    
    finally:
        publisher.disconnect()

def interactive_publisher():
    """Interactive Redis publisher"""
    publisher = MockRedisPublisher()
    
    if not publisher.connect():
        print("❌ Cannot connect to Redis")
        return
    
    print(f"\n📤 Interactive Redis Publisher")
    print("Commands:")
    print("  pub <channel> <message> - Publish message to channel")
    print("  batch - Publish batch of test messages")
    print("  periodic <channel> <interval> <count> - Periodic publishing")
    print("  stats - Show publisher statistics")
    print("  exit - Exit publisher mode")
    
    try:
        while True:
            command = input("\nPublisher> ").strip().split(None, 2)
            
            if not command:
                continue
            
            cmd = command[0].lower()
            
            if cmd == 'exit':
                break
            elif cmd == 'pub' and len(command) >= 3:
                channel = command[1]
                message = command[2]
                
                try:
                    # Try to parse as JSON
                    message_data = json.loads(message)
                except json.JSONDecodeError:
                    # Use as string
                    message_data = message
                
                publisher.publish(channel, message_data)
                
            elif cmd == 'batch':
                messages = [
                    ('test', {'type': 'batch', 'id': 1}),
                    ('test', {'type': 'batch', 'id': 2}),
                    ('test', {'type': 'batch', 'id': 3}),
                ]
                count = publisher.publish_multiple(messages)
                print(f"Published {count} batch messages")
                
            elif cmd == 'periodic' and len(command) >= 2:
                channel = command[1] if len(command) > 1 else 'test'
                interval = float(command[2]) if len(command) > 2 else 1.0
                count = int(command[3]) if len(command) > 3 else 5
                
                publisher.publish_periodic(channel, 'Periodic message', interval, count)
                
            elif cmd == 'stats':
                stats = publisher.get_statistics()
                print(json.dumps(stats, indent=2))
                
            else:
                print("❌ Invalid command")
                
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        publisher.disconnect()
        print("\n👋 Publisher session ended!")

def stress_test():
    """Stress test the publisher"""
    print("Redis Publisher Stress Test")
    print("=========================")
    
    publisher = MockRedisPublisher()
    
    if not publisher.connect():
        print("❌ Cannot connect to Redis")
        return
    
    print("🚀 Publishing 1000 messages across multiple channels...")
    
    channels = ['channel1', 'channel2', 'channel3', 'channel4', 'channel5']
    messages_per_channel = 200
    
    start_time = time.time()
    
    for channel in channels:
        for i in range(messages_per_channel):
            message = {
                'channel': channel,
                'message_id': i + 1,
                'payload': f'Stress test message {i + 1}',
                'timestamp': datetime.now().isoformat()
            }
            publisher.publish(channel, message)
            
            if i % 50 == 0:  # Progress indicator
                print(f"   {channel}: {i + 1}/{messages_per_channel}")
    
    end_time = time.time()
    duration = end_time - start_time
    total_messages = len(channels) * messages_per_channel
    
    stats = publisher.get_statistics()
    
    print(f"✅ Stress test completed!")
    print(f"   Total messages: {total_messages}")
    print(f"   Duration: {duration:.2f} seconds")
    print(f"   Messages per second: {total_messages/duration:.2f}")
    print(f"   Channels used: {len(channels)}")
    
    publisher.disconnect()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == 'interactive':
            interactive_publisher()
        elif mode == 'stress':
            stress_test()
        else:
            print("Available modes: interactive, stress")
    else:
        demo_redis_publisher()