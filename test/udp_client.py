#!/usr/bin/python3

import sys

sys.path.insert(1, '../src')

import udp
udp.PACKET_SIZE = 16

sock = udp.open('', 8081)
pack = bytes('chrissx is cool.', 'utf-8')
print(udp.send(sock, pack, '127.0.0.1', 8081))
udp.close(sock)
