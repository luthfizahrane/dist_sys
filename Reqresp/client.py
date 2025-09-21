#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 14:09:52 2024

@author: widhi
"""

import socket

def client_program():
    client_socket = socket.socket()  
    # Use docker compose service DNS name
    client_socket.connect(('reqresp-server', 2222))

    message = input("Enter message: ")

    while message.lower().strip() != 'exit':
        print(type(message.encode()))
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()

        print('Received from server:', data)

        # Prompt user for next action
        if message.lower().strip() == "book ticket":
            print("Type 'exit' to quit or 'book ticket' to book another ticket.")
        message = input("Enter message: ")

    client_socket.close()

if __name__ == '__main__':
    client_program()
