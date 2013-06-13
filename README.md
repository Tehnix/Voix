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

<table>
  <tr>
    <th>Message</th>
    <th>Explanation</th>
  </tr>
  <tr>
    <td>`>>>` CONNECT: "Nickname" "Real Name" 1.0.0</td>
    <td>Connect to the server with a nickname, real name and the version number</td>
  </tr>
  <tr>
    <td>ACCEPT: hostname.com</td>
    <td>Acknowledge the connection</td>
  </tr>
  <tr>
    <td>PING: 14139282</td>
    <td>The server pings the connection with a random number to check if it is available</td>
  </tr>
  <tr>
    <td>`>>>` PONG: 14139282</td>
    <td>The client responds with PONG and the random number used in the PING</td>
  </tr>
  <tr>
    <td>JOINED: #Lobby</td>
    <td>Inform of the default room that the client is thrown into</td>
  </tr>
  <tr>
    <td>USERLIST #Lobby: John, Michael, Willy</td>
    <td>Return of list of users in the specified room</td>
  </tr>
  <tr>
    <td>`>>>` PRIVMSG #Lobby: Hey all!</td>
    <td>Send a message to the room #Lobby</td>
  </tr>
  <tr>
    <td>PRIVMSG #Lobby: Hey Nickname!</td>
    <td>Receive a message from the room #Lobby</td>
  </tr>
  <tr>
    <td>`>>>` PRIVMSG John: Hey John!</td>
    <td>Send a message to the user, John</td>
  </tr>
  <tr>
    <td>PRIVMSG John: Hey there :)</td>
    <td>Receive a message from the user John</td>
  </tr>
  <tr>
    <td>`>>>` TALK John: Request</td>
    <td>Request a VoIP conversation with John</td>
  </tr>
  <tr>
    <td>TALK John: Accept</td>
    <td>John accepts the VoIP call, which is started in a new thread and kept separate from the main thread</td>
  </tr>
  <tr>
    <td>`>>>` Talk John: End</td>
    <td>End the VoIP call with John</td>
  </tr>
  <tr>
    <td>PING: 42231233</td>
    <td>The server pings the connection with a random number to check if it is available</td>
  </tr>
  <tr>
    <td>`>>>` PONG: 42231233</td>
    <td>The client responds with PONG and the random number used in the PING</td>
  </tr>
  <tr>
    <td>`>>>` JOIN: #TurboRoom</td>
    <td>Join a room named #TurboRoom</td>
  </tr>
  <tr>
    <td>JOINED: #TurboRoom</td>
    <td>The server confirms the join</td>
  </tr>
  <tr>
    <td>USERLIST #Lobby: Tina, Mike</td>
    <td>Return of list of users in the specified room</td>
  </tr>
  <tr>
    <td>TALK Michael: Request</td>
    <td>Get a request from Michael to start a VoIP call</td>
  </tr>
  <tr>
    <td>`>>>` TALK Michael: Deny</td>
    <td>Deny the VoIP request from Michael</td>
  </tr>
  <tr>
    <td>TALK Michael: Request</td>
    <td>Get a request from Michael to start a VoIP call</td>
  </tr>
  <tr>
    <td>`>>>` TALK Michael: Accept</td>
    <td>Accept the VoIP call from Michael, a new thread and kept separate from the main thread</td>
  </tr>
  <tr>
    <td>TALK Michael: End</td>
    <td>Michael ends the call</td>
  </tr>
  <tr>
    <td>`>>>` DISCONNECT</td>
    <td>Disconnect from the server</td>
  </tr>
</table>


