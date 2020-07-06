# "CSP" (chrissx shaun protocol)

The CSP is a protocol designed to allow Schafkopf players' clients to
communicate with a central server.

# Packets

```
PACKET_SIZE = 32
nullpack = [0] * PACKET_SIZE
onepack = [1] * PACKET_SIZE
```

If any of the parameters are determined to be wrong by the server,
`nullpack` is returned.

Packet id|Parameter 1|Parameter 2|Description|Returned packet
---|---|---|---|---
0x00|–|–|Does nothing.|`nullpack`
0x01|–|–|Handshake (fails if 24 players are logged in)|`if failed: nullpack, if success: pid + [0] * (PACKET_SIZE - 1)`
0x02|pid|–|Votestart (vote to start or not)|votestart = true: `onepack`, votestart = false: `nullpack`
0x03|pid|–|Get the current game status and player's hand|`[1] * 2 + [game is running ? 1 : 0] * 2 + [is player's turn ? 1 : 0] * 2 + cards on players hand + [0] * remaining byte count`
0x04|pid|–|Get the pids of all players|`[1] * 8 + all players' pids + [0] * remaining byte count`
0x05|pid|other pid|Get player name|`[1] * 2 + name(other pid) + [0] * remaining byte count`
0x06|pid|–|Get stack|`[1] * 8 + stack + [0] * remaining byte count`
0x07|pid|name|Set name|`onepack`
0x08|–|–|
