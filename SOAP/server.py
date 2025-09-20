#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:49:40 2024

@author: widhi
"""

from spyne import Application, rpc, ServiceBase, Unicode, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

# Membuat layanan SOAP dengan metode penjumlahan
class CalculatorService(ServiceBase):
    @rpc(Integer, Integer, _returns=Integer)
    def add(ctx, a, b):
        return a + b

# Membuat layanan SOAP dengan metode menghitung jumlah kata
class StringService(ServiceBase):
    @rpc(Unicode, _returns=Integer)
    def word_count(ctx, text):
        return len(text.split())

# Membuat aplikasi SOAP dengan protokol Soap11
app = Application([CalculatorService, StringService],
                  tns='spyne.examples.calculator',
                  in_protocol=Soap11(),
                  out_protocol=Soap11())

# Menjalankan server menggunakan WSGI
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(app)
    # Bind on all interfaces for container networking
    server = make_server('0.0.0.0', 8080, wsgi_app)
    print("SOAP server listening on http://0.0.0.0:8080 (service DNS: soap-server:8080)")
    server.serve_forever()
