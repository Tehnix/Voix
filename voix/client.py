#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The main client.

"""
import logging
import socket


class Client(object):
    """Client object."""

    def __init__(self):
        """
        Initializes the client object

        """
        super(Client, self).__init__()
        self.host = None
        self.port = 10000
        self.nick = None
        self.actions = {'HOST': self.set_host,
                        'PORT': self.set_port,
                        'NICK': self.set_nickname,
                        'CONNECT': self.connect,
                        'PONG': self.pong}

    def perform_action(self, action):
        """
        Performs the provided `action`.

        Arguments:
        - `action`:
        The action to perform, an example could be to set the host
        which the client connects to. "HOST 127.0.0.1" would set the
        host setting.
        """
        command = action.split()[0]
        value = " ".join(action.split()[1:])
        func = self.actions.get(command)
        try:
            func(value)
        except Warning as warn:
            logging.warning(warn)

    def set_host(self, host):
        """
        Sets the value of a given field.

        Arguments:
        - `field`:
        The field to set the given `value`.
        - `value`:
        The value to set.
        """
        logging.debug('Host set to {0}'.format(host))
        self.host = host

    def set_port(self, port):
        """
        Sets the value of a given field.

        Arguments:
        - `field`:
        The field to set the given `value`.
        - `value`:
        The value to set.
        """
        logging.debug('Port set to {0}'.format(port))
        self.port = port

    def set_nickname(self, nick):
        """
        Sets the value of a given field.

        Arguments:
        - `field`:
        The field to set the given `value`.
        - `value`:
        The value to set.
        """
        logging.debug('Port set to {0}'.format(nick))
        self.nick = nick

    def connect(self, value = ''):
        """
        Connects to the server if both hostname and username is set.

        """
        if self.host is None or self.nick is None:
            raise Warning('You must set the server\'s hostname and your name before connecting')

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))



    def pong(self, value = ''):
        """
        Connects to the server if both hostname and username is set.

        """
        if self.host is None or self.nick is None:
            raise Warning('You must be connected, before you can ping.')

    def close(self):
        """Wrapper for the sockets close function."""
        if self.sock:
            return self.sock.close()
        else:
            return
