#!/usr/bin/env python3
"""
HTTP/REST Server Example
Implementasi server REST API sederhana untuk sistem terdistribusi
"""

from flask import Flask, jsonify, request
import json
import time
from datetime import datetime

app = Flask(__name__)

# In-memory storage for demo purposes
users = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"}
}

messages = []

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        "service": "HTTP REST API Server",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "GET /users - List all users",
            "GET /users/<id> - Get specific user",
            "POST /users - Create new user",
            "PUT /users/<id> - Update user",
            "DELETE /users/<id> - Delete user",
            "GET /messages - List messages",
            "POST /messages - Send message"
        ]
    })

@app.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    return jsonify(list(users.values()))

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user by ID"""
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    """Create new user"""
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400
    
    new_id = max(users.keys()) + 1 if users else 1
    new_user = {
        "id": new_id,
        "name": data['name'],
        "email": data['email']
    }
    users[new_id] = new_user
    
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update existing user"""
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    user = users[user_id]
    user.update({k: v for k, v in data.items() if k in ['name', 'email']})
    
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    del users[user_id]
    return jsonify({"message": "User deleted successfully"})

@app.route('/messages', methods=['GET'])
def get_messages():
    """Get all messages"""
    return jsonify(messages)

@app.route('/messages', methods=['POST'])
def send_message():
    """Send a message"""
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "Message content is required"}), 400
    
    message = {
        "id": len(messages) + 1,
        "content": data['content'],
        "sender": data.get('sender', 'anonymous'),
        "timestamp": datetime.now().isoformat()
    }
    messages.append(message)
    
    return jsonify(message), 201

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("Starting HTTP/REST Server...")
    print("API Documentation:")
    print("- GET    /users          - List all users")
    print("- GET    /users/<id>     - Get specific user")
    print("- POST   /users          - Create new user")
    print("- PUT    /users/<id>     - Update user")
    print("- DELETE /users/<id>     - Delete user")
    print("- GET    /messages       - List messages")
    print("- POST   /messages       - Send message")
    print("\nServer running on http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)