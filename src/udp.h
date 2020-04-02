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

#ifdef UDP_USE_IPV6
#define _sockaddr_in_udp struct sockaddr6_in
#define _domain_udp AF_INET6
#define _inaddr_any_udp in6addr_any
#else
#define _sockaddr_in_udp struct sockaddr_in
#define _domain_udp AF_INET
#define _inaddr_any_udp INADDR_ANY
#endif

typedef int _socket_udp;

typedef struct _udp {
        _socket_udp      sock;
        _sockaddr_in_udp addr;
} udp;

udp _udp_constructor(_socket_udp sock, _sockaddr_in_udp addr) {
        udp u;
        memcpy(&u.sock, &sock, sizeof(sock));
        memcpy(&u.addr, &addr, sizeof(addr));
        return u;
}

udp udp_open_socket(bool server_mode, uint32_t port) {
        int type = SOCK_DGRAM; //| (server_mode ? SOCK_NONBLOCK : 0);
        int sock = socket(_domain_udp, type, 0);
        _sockaddr_in_udp addr;
        memset(&addr, 0, sizeof(addr));
        addr.sin_family = _domain_udp;
        addr.sin_addr.s_addr = _inaddr_any_udp;
        addr.sin_port = htons(port);
        bind(sock, (const struct sockaddr *) &addr, sizeof(addr));
        return _udp_constructor(sock, addr);
}
