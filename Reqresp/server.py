#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 14:04:45 2024

@author: widhi
"""

import socket

def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to all interfaces so other containers can reach the server
    server_socket.bind(('0.0.0.0', 2222))  
    
    server_socket.listen(1)
    print("Server listening on 0.0.0.0:2222")
    tickets_available = 5  # Jumlah tiket yang tersedia
    conn, address = server_socket.accept()
    print("Connection from:", address)

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Received from client:", data)

        # Proses pemesanan tiket
        if data.lower() == "book ticket":
            if tickets_available > 0:
                tickets_available -= 1
                response = f"Booking successful! Tickets remaining: {tickets_available}"
            else:
                response = "Booking failed! No tickets available."
        else:
            response = "Invalid request. Please send 'book ticket' to book."
        conn.send(response.encode())

    conn.close()

if __name__ == '__main__':
    server_program()
