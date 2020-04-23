#!/usr/bin/python3

import sys
import udp
from random import SystemRandom
udp.PACKET_SIZE = 16

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

sock = udp.open('127.0.0.1', 4269)

players = []
running = False
all_cards = [0x8b, 0x8a, 0x84, 0x83, 0x82, 0x80,
             0x4b, 0x4a, 0x44, 0x43, 0x42, 0x40,
             0x2b, 0x2a, 0x24, 0x23, 0x22, 0x20,
             0x1b, 0x1a, 0x14, 0x13, 0x12, 0x10]
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
    return rand(0, 255)

def rand(start, end):
    return SystemRandom().randint(start, end)

def choice(x):
    return SystemRandom().choice(x)

def has_player_id(pid):
    for p in players:
        if p.id == pid:
            return True
    return False

def get_player(pid):
    for p in players:
        if p.pid == pid:
            return players.index(p)
    return -1

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
            players.append({'pid':pid,'cards':[],startvote:False})
            udp.answer(sock, bytes(pid), client)
    else:
        pid = packet[1]
        if pid == 0 or not has_player_id(pid):
            answer = udp.nullpack()
        else:
            if packid == 2:
                players[get_player(pid)].startvote = True
                answer = [1] * udp.PACKET_SIZE
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
    else if players in [2, 3, 4, 6, 8, 12, 24]:
        start = True
        for p in players:
            if not p.startvote:
                start = False
        if start:
            available_cards = all_cards.copy()
            while len(available_cards) > 0:
                for p in players:
                    card = choice(available_cards)
                    available_cards.remove(card)
                    p.cards.append(card)
    return True

b = True

while b:
    handle_packet(udp.accept(sock))
    b = tick_game()

udp.close(sock)
