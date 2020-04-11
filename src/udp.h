#include <string.h>
#include <stdint.h>
#include <stdlib.h>

#ifdef __linux__
# include <sys/types.h>
# include <sys/socket.h>
# include <netinet/in.h>
# include <arpa/inet.h>
# include <netinet/in.h>
#else
# include <Windows.h>
#endif

#ifndef bool
typedef int bool;
#endif

#ifndef UDP_PACKET_SIZE
# define UDP_PACKET_SIZE 16
#endif

#ifdef UDP_USE_IPV6
# define _sockaddr_in_udp struct sockaddr_in6
# define _in_addr_udp struct in6_addr
# define _domain_udp AF_INET6
# define _inaddr_any_udp in6addr_any
# define _sinaddr_udp sin6_addr
# define _sin_family_udp sin6_family
# define _sin_addr_udp sin6_addr
# define _s_addr_udp s6_addr
# define _sin_port_udp sin6_port
# define _port_udp uint32_t
# define _set_s_addr_udp(dst, val) memcpy(dst, val, sizeof(dst));
#else
# define _sockaddr_in_udp struct sockaddr_in
# define _in_addr_udp in_addr_t
# define _domain_udp AF_INET
# define _inaddr_any_udp INADDR_ANY
# define _sinaddr_udp sin_addr
# define _sin_family_udp sin_family
# define _sin_addr_udp sin_addr
# define _s_addr_udp s_addr
# define _sin_port_udp sin_port
# define _port_udp uint32_t
# define _set_s_addr_udp(dst, val) dst = val;
#endif

typedef int _socket_udp;

typedef struct _udp {
        _socket_udp      sock;
        _sockaddr_in_udp addr;
} udp;

typedef struct _udp_packet {
        char bfr[UDP_PACKET_SIZE];
        size_t len = UDP_PACKET_SIZE;
} udp_packet;

typedef struct _udp_packet_with_sockaddr {
        udp_packet      packet;
        struct sockaddr skaddr;
} udp_packet_with_sockaddr;

udp _udp_constructor(_socket_udp sock, _sockaddr_in_udp addr) {
        udp u;
        memcpy(&u.sock, &sock, sizeof(sock));
        memcpy(&u.addr, &addr, sizeof(addr));
        return u;
}

_sockaddr_in_udp _sockaddr_in_constructor(_in_addr_udp addr, _port_udp port) {
        _sockaddr_in_udp a;
        memset(&addr, 0, sizeof(addr));
        a._sin_family_udp = _domain_udp;
        _set_s_addr_udp(a._sin_addr_udp._s_addr_udp, addr);
        a._sin_port_udp = htons(port);
        return a;
}

//server_addr = 0 if running as server
udp udp_open_socket(_in_addr_udp server_addr, _port_udp port) {
        int type = SOCK_DGRAM; //| (!server_addr ? SOCK_NONBLOCK : 0);
        int sock = socket(_domain_udp, type, 0);
        _sockaddr_in_udp addr = _sockaddr_in_constructor(server_addr ? server_addr : _inaddr_any_udp, port);
        if(server_addr)
                bind(sock, (const struct sockaddr *) &addr, sizeof(addr));
        return _udp_constructor(sock, addr);
}

udp_packet udp_send(udp u, udp_packet packet, _in_addr_udp dest, _port_udp port) {
        _sockaddr_in_udp dst = _sockaddr_in_constructor(dest, port);
        sockaddr *sa = (sockaddr *) &dst;
        socklen_t sasize = sizeof(dst);
        sendto(u.sock, packet.bfr, packet.len, MSG_CONFIRM, sa, sasize);
        udp_packet answer;
        recvfrom(u.sock, answer.bfr, answer.len, MSG_WAITALL, sa, &sasize);
        return answer;
}

udp_packet_with_sockaddr udp_accept(udp u) {
        udp_packet_with_sockaddr packet;
        socklen_t addrlen;
        recvfrom(u.sock, packet.packet.bfr, packet.packet.len,
                 MSG_WAITALL, &packet.skaddr, &addrlen);
        return packet;
}
