VoIP
===================
### Stuffz ###
* Connect til server (aka, ikke P2P)
* Privat samtale (one-on-one)
* Lobby - alle snakker sammen her
* Chat rum / gruppe chat

### Extra stuffz ###
* Sideløbende IM (En del af TCP kanalen)

### Implementation ###
* Kig på PyAudio (+ wrapper til speex)
* UDP -> Voice channel, TCP -> Signalling channel

### Protocol ###
For quickness, I will use `>>>` to indicate client input, and server response is with nothing prepended (kindda like output in a REPL).

A client shall *always* connect with a nickname, no spaces or `"` allowed though. A nickname must be unique!

A channel is denoted with # prepended to it.

Example of a run:

>>> CONNECT: "Nickname" "Real Name" 1.0.0      | Connect to the server with a nickname, real name and the version number
ACCEPT: hostname.com                           | Acknowledge the connection
PING: 14139282                                 | The server pings the connection with a random number to check if it is available
>>> PONG: 14139282                             | The client responds with PONG and the random number used in the PING
JOINED: #Lobby                                 | Inform of the default room that the client is thrown into
USERLIST #Lobby: John, Michael, Willy          | Return of list of users in the specified room
>>> PRIVMSG #Lobby: Hey all!                   | Send a message to the room #Lobby
PRIVMSG #Lobby: Hey Nickname!                  | Receive a message from the room #Lobby
>>> PRIVMSG John: Hey John!                    | Send a message to the user, John
PRIVMSG John: Hey there :)                     | Receive a message from the user John
>>> TALK John: Request                         | Request a VoIP conversation with John
TALK John: Accept                              | John accepts the VoIP call, which is started in a new thread and kept separate from the main thread
>>> Talk John: End                             | End the VoIP call with John
PING: 42231233                                 | The server pings the connection with a random number to check if it is available
>>> PONG: 42231233                             | The client responds with PONG and the random number used in the PING
>>> JOIN: #TurboRoom                           | Join a room named #TurboRoom
JOINED: #TurboRoom                             | The server confirms the join
USERLIST #Lobby: Tina, Mike                    | Return of list of users in the specified room
TALK Michael: Request                          | Get a request from Michael to start a VoIP call
>>> TALK Michael: Deny                         | Deny the VoIP request from Michael
TALK Michael: Request                          | Get a request from Michael to start a VoIP call
>>> TALK Michael: Accept                       | Accept the VoIP call from Michael, a new thread and kept separate from the main thread
TALK Michael: End                              | Michael ends the call
>>> DISCONNECT                                 | Disconnect from the server

