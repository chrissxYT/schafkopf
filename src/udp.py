#!/usr/bin/python3

import socket

if UDP_PACKET_SIZE == 0:
    UDP_PACKET_SIZE = 16

def udp_open_socket(host, port):
    if UDP_USE_IPV6:
        sock = socket.socket(AF_INET6, SOCK_DGRAM)
    else:
        sock = socket.socket(AF_INET, SOCK_DGRAM)
    if host != 0:
        addr = (host, port)
        sock.bind(addr)
    else:
        addr = ('', port) # this probably wont work with ipv6, but i
                          # dont know a way to fix this right now
    return (sock, addr)

def udp_send(udp, packet, dest, port):
    dst = (dest, port)
    udp[0].sendto(packet, MSG_CONFIRM, dst)
    answer, _ = udp[0].recvfrom(UDP_PACKET_SIZE, MSG_WAITALL)
    return answer;

def udp_accept(udp):
    return recvfrom(UDP_PACKET_SIZE, MSG_WAITALL)

def udp_answer(udp, packet, dst):
    udp[0].sendto(packet, MSG_CONFIRM, dst)
