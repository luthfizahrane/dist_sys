#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:52:27 2024

@author: widhi
"""
from zeep import Client

# URL WSDL menggunakan nama service Docker Compose
wsdl = 'http://soap-server:8000/?wsdl'

# Membuat klien SOAP berdasarkan WSDL
client = Client(wsdl=wsdl)

# Memanggil metode penjumlahan dari layanan SOAP server
result = client.service.word_count("Hello, Luthfi Zahran!")

# Menampilkan hasil penjumlahan
print(f'Jumlah kata: {result}')

