#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 17:05:25 2024

@author: widhi
"""

import requests
import argparse
import sys

BASE = 'http://rest-server:5151'

def call(endpoint, a, b=None):
    try:
        params = {'a': a}
        if b is not None:
            params['b'] = b
        print(f"Calling {endpoint} with params: {params}")
        r = requests.get(f"{BASE}/{endpoint}", params=params, timeout=3)
        if r.status_code == 200:
            data = r.json()
            print(f"{endpoint}({a},{b}) = {data['result']}")
        else:
            print(f"{endpoint} error {r.status_code}: {r.text}")
    except Exception as e:
        print(f"{endpoint} exception: {e}")

def main():
    parser = argparse.ArgumentParser(description="Simple REST client for math endpoints")
    parser.add_argument('--op', choices=['add', 'mul', 'sub', 'div', 'pow', 'fact', 'mod', 'both'], default='both', help='Operation to invoke')
    parser.add_argument('-a', type=int, required=True)
    parser.add_argument('-b', type=int, required=True)
    args = parser.parse_args()
    if args.op in ('add', 'both'):
        call('add', args.a, args.b)
    if args.op in ('mul', 'both'):
        call('mul', args.a, args.b)
    if args.op in ('sub', 'both'):
        call('sub', args.a, args.b)
    if args.op in ('div', 'both'):
        call('div', args.a, args.b)
    if args.op in ('pow', 'both'):
        call('pow', args.a, args.b)
    if args.op in ('fact', 'both'):
        call('fact', args.a)
    if args.op in ('mod', 'both'):
        call('mod', args.a, args.b)

if __name__ == '__main__':
    sys.exit(main())
