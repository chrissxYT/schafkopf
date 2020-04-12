#!/usr/bin/python3

import socket
PACKET_SIZE = 16
USE_IPV6 = False

def open_socket(host, port):
    if USE_IPV6:
        sock = socket.socket(AF_INET6, SOCK_DGRAM)
    else:
        sock = socket.socket(AF_INET, SOCK_DGRAM)
    addr = (host, port)
    if host != '':
        sock.bind(addr)
    return (sock, addr)

def send(udp, packet, dest, port):
    dst = (dest, port)
    udp[0].sendto(packet, MSG_CONFIRM, dst)
    answer, _ = udp[0].recvfrom(PACKET_SIZE, MSG_WAITALL)
    return answer;

def accept(udp):
    return recvfrom(PACKET_SIZE, MSG_WAITALL)

def answer(udp, packet, dst):
    udp[0].sendto(packet, MSG_CONFIRM, dst)
