#!/usr/bin/python3

import sys
import udp
from random import SystemRandom
udp.PACKET_SIZE = 16

sock = udp.open('127.0.0.1', 4269)

players = []

Eichel = 'e'
Blatt = 'b'
Herz = 'h'
Schelle = 's'
Ober = 'o'
Unter = 'u'

trumpf = [Ober, Unter, Herz]

def is_of_type(typ, card):
    if typ == Eichel and card & 0x80 == 0x80:
        return True
    if typ == Blatt and card & 0x40 == 0x40:
        return True
    if typ == Herz and card & 0x20 == 0x20:
        return True
    if typ == Schelle and card & 0x10 == 0x10:
        return True
    if typ == Ober and card & 3 == 3:
        return True
    if typ == Unter and card & 2 == 2:
        return True
    return False

def is_trumpf(card):
    for t in trumpf:
        if(is_of_type(t, card)):
            return True
    return False

def has_trumpf(cards):
    for c in cards:
        if is_trumpf(c):
            return True
    return False

def max_trumpf(t, c):
    if t == 0:
        return c
    if c == 0:
        return t
    tl = t & 0x0f
    cl = c & 0x0f
    th = t & 0xf0
    ch = c & 0xf0
    if tl == 3 and cl == 2:
        return t
    if tl == 2 and cl == 3:
        return c
    if tl == 3 and cl == 3:
        if th > ch:
            return t
        else:
            return c
    if tl == 2 and tl == 2:
        if th > ch:
            return t
        else:
            return c
    if tl > cl:
        return t
    else:
        return c

def max_farbe(t, c):
    tl = t & 0x0f
    cl = c & 0x0f
    th = t & 0xf0
    ch = c & 0xf0
    if th != ch:
        return t
    if tl > cl:
        return t
    else:
        return c

def highest_farbe(cards):
    t = cards[0]
    for c in cards:
        t = max_farbe(t, c)
    return t

def highest_trumpf(cards):
    t = cards[0]
    for c in cards:
        if is_trumpf(c):
            t = max_trumpf(t, c)
    return t

def round_winner(cards):
    if(has_trumpf(cards)):
        return highest_trumpf(cards)
    else:
        return highest_farbe(cards[0], cards)

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
