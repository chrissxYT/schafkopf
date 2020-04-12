#!/usr/bin/python3

from socket import *
PACKET_SIZE = 16
USE_IPV6 = False

def open(host = '', port = 0):
    if USE_IPV6:
        sock = socket(AF_INET6, SOCK_DGRAM)
    else:
        sock = socket(AF_INET, SOCK_DGRAM)
    if host != '':
        sock.bind((host, port))
    return sock

def send(sock, packet, dest, port):
    dst = (dest, port)
    sock.sendto(packet, MSG_CONFIRM, dst)
    answer, _ = sock.recvfrom(PACKET_SIZE, MSG_WAITALL)
    return answer;

def accept(sock):
    return sock.recvfrom(PACKET_SIZE, MSG_WAITALL)

def answer(sock, packet, dst):
    sock.sendto(packet, MSG_CONFIRM, dst)

def close(sock):
    sock.close()
