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
