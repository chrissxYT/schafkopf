#!/usr/bin/python3

import sys
import udp
from random import SystemRandom
udp.PACKET_SIZE = 16

sock = udp.open('127.0.0.1', 4269)

players = []

def generate_player_id():
    return SystemRandom().randint(0, 255)

def has_player_id(pid):
    for p in players:
        if p.id == pid:
            return True
    return False

def handle_packet(packet, client):
    print('Got packet: "{}" from "{}"'.format(packet.hex(), client))
    packid = packet[0]
    if packid == 0:
        udp.sendnull(sock, client)
    else if packid == 1:
        if len(players) > 250:
            udp.sendnull(sock, client)
        pid = generate_player_id()
        while has_player_id(pid) or pid == 0:
            pid = generate_player_id()
        players.append({'pid':pid,'cards':[]})
        udp.answer(sock, bytes([SystemRandom().randint(0, 255)]), client)

def tick_game():
    return True

b = True

while b:
    handle_packet(udp.accept(sock))
    b = tick_game()

udp.close(sock)
