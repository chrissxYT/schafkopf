#!/usr/bin/python3

import sys
import udp
from random import SystemRandom
udp.PACKET_SIZE = 16

sock = udp.open('127.0.0.1', 4269)

players = []
running = False

Eichel = 'e'
Blatt = 'b'
Herz = 'h'
Schelle = 's'
Ober = 'o'
Unter = 'u'
Ass = 'a'
Ten = '10'
König = 'k'
Nine = '9'

trumpf = [Ober, Unter, Herz]

def is_of_type(typ, card):
    lo = card & 0x0f
    hi = card & 0xf0
    if typ == Eichel and hi == 0x80:
        return True
    if typ == Blatt and hi == 0x40:
        return True
    if typ == Herz and hi == 0x20:
        return True
    if typ == Schelle and hi == 0x10:
        return True
    if typ == Ober and lo == 3:
        return True
    if typ == Unter and lo == 2:
        return True
    if typ == Ass and lo == 11:
        return True
    if typ == Ten and lo == 10:
        return True
    if typ == König and lo == 4:
        return True
    if typ == Nine and lo == 0:
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

def highest_farbe(cards):
    t = cards[0]
    for c in cards:
        if t & 0xf0 == c & 0xf0 and c > t:
            t = c
    return t

def highest_trumpf(cards):
    t = cards[0]
    for c in cards:
        if is_trumpf(c):
            th = t & 0xf0
            ch = c & 0xf0
            tl = t & 0x0f
            cl = c & 0x0f
            if tl == 2 and cl == 3:
                t = c
            else if tl == cl and c > t:
                t = c
            else if tl not in [2, 3] and cl not in [2, 3] and c > t:
                t = c
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
    print('Incoming: "{}" from "{}"'.format(packet.hex(), client))
    packid = packet[0]
    if packid == 0:
        answer = udp.nullpack()
    else if packid == 1:
        if len(players) > 250:
            answer = udp.nullpack()
        else:
            pid = 0
            while pid == 0 or has_player_id(pid):
                pid = generate_player_id()
            players.append({'pid':pid,'cards':[]})
            udp.answer(sock, bytes(pid), client)
    else:
        pid = packet[1]
        if not has_player_id(pid) or pid == 0:
            answer = udp.nullpack()
        else:
    print('Outgoing: "{}" to "{}"'.format(answer.hex(), client))
    udp.answer(sock, answer, client)

def tick_game():
    if running:
        ended = True
        for p in players:
            if len(p.cards) == 0:
                ended = False
        if ended:
            return False
    else if 24 % players == 0 and False:
        start()
    return True

b = True

while b:
    handle_packet(udp.accept(sock))
    b = tick_game()

udp.close(sock)
