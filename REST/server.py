#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 17:02:45 2024

@author: widhi
"""

from flask import Flask, request, jsonify

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Endpoint untuk penjumlahan
@app.route('/add', methods=['GET'])
def add_numbers():
    try:
        # Mengambil parameter a dan b dari query string
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        result = a + b
        
        # Mengembalikan hasil dalam format JSON
        return jsonify({'result': result})
    except (TypeError, ValueError):
        # Menangani error jika input tidak valid
        return jsonify({'error': 'Invalid input'}), 400
    
@app.route('/mul', methods=['GET'])
def mul_numbers():
    try:
        # Mengambil parameter a dan b dari query string
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        result = a * b
        
        # Mengembalikan hasil dalam format JSON
        return jsonify({'result': result})
    except (TypeError, ValueError):
        # Menangani error jika input tidak valid
        return jsonify({'error': 'Invalid input'}), 400
    
@app.route('/sub', methods=['GET'])
def sub_numbers():
    try:
        # Mengambil parameter a dan b dari query string
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        result = a - b

        # Mengembalikan hasil dalam format JSON
        return jsonify({'result': result})
    except (TypeError, ValueError):
        # Menangani error jika input tidak valid
        return jsonify({'error': 'Invalid input'}), 400

@app.route('/div', methods=['GET'])
def div_numbers():
    try:
        # Mengambil parameter a dan b dari query string
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        result = a / b

        # Mengembalikan hasil dalam format JSON
        return jsonify({'result': result})
    except (TypeError, ValueError):
        # Menangani error jika input tidak valid
        return jsonify({'error': 'Invalid input'}), 400
        
@app.route('/pow', methods=['GET'])
def pow_numbers():
    try:
        # Mengambil parameter a dan b dari query string
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        result = a ** b

        # Mengembalikan hasil dalam format JSON
        return jsonify({'result': result})
    except (TypeError, ValueError):
        # Menangani error jika input tidak valid
        return jsonify({'error': 'Invalid input'}), 400


@app.route('/fact', methods=['GET'])
def fact_number():
    try:
        # Mengambil parameter a dari query string
        a = int(request.args.get('a'))
        if a < 0:
            return jsonify({'error': 'Negative input not allowed'}), 400
        result = 1
        for i in range(2, a + 1):
            result *= i

        # Mengembalikan hasil dalam format JSON
        return jsonify({'result': result})
    except (TypeError, ValueError):
        # Menangani error jika input tidak valid
        return jsonify({'error': 'Invalid input'}), 400

@app.route('/mod', methods=['GET'])
def mod_numbers():
    try:
        # Mengambil parameter a dan b dari query string
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        result = a % b

        # Mengembalikan hasil dalam format JSON
        return jsonify({'result': result})
    except (TypeError, ValueError):
        # Menangani error jika input tidak valid
        return jsonify({'error': 'Invalid input'}), 400
 
# Jalankan server di port 5000
if __name__ == '__main__':
    # Bind to 0.0.0.0 so container port mapping works externally
    app.run(debug=True, host='0.0.0.0', port=5151)
