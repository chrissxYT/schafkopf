#!/usr/bin/python3

import sys

sys.path.insert(1, '../src')

import udp
udp.PACKET_SIZE = 16

sock = udp.open('127.0.0.1', 8081)
pack = bytes('chrissx is lool.', 'utf-8')
req, cli = udp.accept(sock)
print(req)
udp.answer(sock, pack, cli)
udp.close(sock)
