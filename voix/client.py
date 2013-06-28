#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The main client object.

"""
import logging
import socket

from version import get_git_version
from connection import Connection
from parser import Parser
from interface.cli import CLI
from interface.gui import GUI
from message_handler import MessageHandler


class Client(object):
    """Client object."""

    def __init__(self):
        """
        Initializes the client object
        """
        super(Client, self).__init__()

        self.host = None
        self.port = '10000'

        self.nick = None
        self.name = None

        self.parser = Parser(self)

        self.message_handler = MessageHandler()
        self.update_callback = None

        self.tcp = Connection(self, 'TCP')
        self.udp = Connection(self, 'UDP')

    def register_update_callback(self, func):
        """
        """
        self.update_callback = func

    def set_host(self, data):
        """
        Sets the value of a given field.

        Arguments:
        - `field`:
        The field to set the given `value`.
        - `value`:
        The value to set.
        """

        host = data[2]

        logging.debug('Host set to {0}'.format(host))
        self.host = host

    def set_port(self, data):
        """
        Sets the value of a given field.

        Arguments:
        - `field`:
        The field to set the given `value`.
        - `value`:
        The value to set.
        """
        port = data[2]
        logging.debug('Port set to {0}'.format(port))
        self.port = port

    def connect(self, data):
        """
        Connects to the server if both hostname and username is set.

        """
        if self.host is None:
            raise Warning(' '.join(['You must set the server\'s',
                                    'hostname and your name before',
                                    'connecting']))

        self.nick = data[2].split()[0]
        name = ' '.join(data[2].split()[1:])
        try:
            self.tcp.connect((self.host, int(self.port)))
        except socket.error as e:
            return self.denied([e.strerror])
        self.tcp.send(
            bytes('CONNECT: "{0}" "{1}" {2}\r\n'.format(self.nick,
                                                        name,
                                                        get_git_version()))
        )
        self.tcp.handle.start()

    def pong(self, data):
        if not self.tcp.is_connected():
            raise Warning('You are not connected!')

        num = data[2]

        self.tcp.send(bytes('PONG: {0}\r\n'.format(num)))

    def join_channel(self, data):
        if not self.tcp.is_connected():
            raise Warning('You are not connected!')

        channel = data[2]
        self.tcp.send(bytes('JOIN: {0}\r\n'.format(channel)))

    def message(self, data):
        """
        Client > Server:
        `MSG #Lobby: Hello there!' (Public message in #Lobby. Sender
        is assigned on server side)
        `MSG John: Hi John!' (Private message. Sender is assigned on
        server side)

        Server > Client:
        `MSG Mike #Lobby: Hello there!' (Public message in
        #Lobby. Sent to all clients in the room.)
        `MSG Mike John: Hi John' (Private message)

        Arguments:
        - `data`:
        Given the scenarios above, data is a list where `data[0]` may
        be a nickname or a channel if `data[1]` is None.
        If `data[1]` is not None, it can either be a channel or a
        nickname. In that case `data[0]` will always be a nickname.

        `data[2]` is always the message.
        """
        if not self.tcp.is_connected():
            raise Warning('You are not connected!')

        chan = None
        recp = None
        sender = None

        if data[1] and '#' in data[1]:
            chan = data[1]
        elif data[1] and not '#' in data[1]:
            recp = data[1]
        elif not data[1]:
            recp = data[0]

        if data[0] and data[1]:
            sender = data[0]

        chatter = sender or recp

        msg = data[2]

        if (not data[0] and data[1]) or (not data[1] and data[0]):
            self.tcp.send(bytes('MSG {0}: {1}\r\n'.format(chan or recp, msg)))

        self.message_handler.message(author=sender,
                                     recipient=recp,
                                     channel=chan,
                                     message=msg)

    def talk(self, data):
        """
        Client > Server:
        `TALK John: Request'

        Server > Client:
        `TALK Mike John: Request' (Private message)

        Arguments:
        - `data`:
        Given the scenarios above, data is a list where `data[0]` is
        always a nickname.
        If `data[1]` is not None, this will be the receiver of the
        code message.

        `data[2]` is always the code i.e. Request, Accept, Deny, End.
        """
        if not self.tcp.is_connected():
            raise Warning('You are not connected!')

        code = data[2]
        recp = ''

        if data[1] is None:
            self.message_handler.talk(responder=data[0], code=code)
        else:
            self.message_handler.talk(requester=data[0],
                                      responder=data[1],
                                      code=code)
            recp = ' %s' % data[1]

        self.tcp.send(bytes('TALK {0}{1}: {2}\r\n'.format(data[0],
                                                          recp,
                                                          data[2])))

        if code == 'Accept':
            self.udp.open_stream()
        elif code == 'End':
            self.udp.close_stream()

    def accepted(self, data):
        self.tcp.connected = True
        logging.debug(
            'Connection to {0} has been established!'.format(data[0])
        )

    def denied(self, data):
        logging.debug(
            'Your attempt to connect failed. Reason: {0}'.format(data[0])
        )

    def joined_channel(self, data):
        self.update_callback(channel=data[2])
        logging.debug('You have joined the channel: '.format(data[2]))

    def userlist(self, data):
        self.update_callback(channel=data[1], userlist=data[2])
        logging.debug('Users on {0}: {1}'.format(data[1], data[2]))

    def close(self):
        """Wrapper for the sockets close function."""
        if self.tcp.sock:
            self.tcp.sock.close()
        if self.udp.sock:
            self.udp.sock.close()
