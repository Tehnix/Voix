## Connect and talk in lobby ##
The client establishes a connection to the server. The client is then
sent to the lobby and may then send voice data to other clients.

## Disconnect ##
The client closes and the server determines that the client has
disconnected.

## Change channel ##
Once in the lobby, the user may switch channel and then all voice data
sent is received by the clients in the new channel.

## Create channel ##
With permission, a user creates a new channel and users may then join
it.

## Delete channel ##
A user deletes a channel and all users in that channel are sent to the
lobby.

## Successfully join locked channel ##
When attempting to enter a locked channel, the user is prompted with
a message and an input field to sent the password to the server. The
password is correct and the user joins the channel.

## Denied access to locked channel ##
Entering an invalid password results in the user remaining in the
current channel.

## Detailed: Connect and talk in lobby ##
Assuming a server is running, the client opens a connection to the
server socket with the known listening port. The client then
identifies itself to the server by sending a `CONNECT:` with 3
parameters: nickname, real_name, version. If the message is correct
and reaches the server, the server responds with `ACCEPT:` followed by
its hostname. Afterwards the server sends the client to the lobby and
tells the client with the message `JOINED: #Lobby`. The client then
sends voice data and all other clients in the lobby receives it.
