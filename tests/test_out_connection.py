#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import unittest
import mox
import random
import sys

from version import get_git_version
from voix.client import Client
from voix.connection import Connection
from voix.interface.cli import CLI

import voix.interface.cli


class ConnectionOutTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.cli = CLI(self.client)
        self.cli.timeout = 2
        self.cli._testing = True

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client.parser.parse('HOST: localhost')
        self.client.port = str(random.randint(9000, 12000))
        self.server.bind(('localhost', int(self.client.port)))
        self.server.listen(5)

        self.client.parser.parse('CONNECT: joe Cake Man')
        self.con, addr = self.server.accept()
        self.data = self.con.recv(1024)
        self.client.tcp.connected = True

    def test_client_connect_to_server(self):
        self.assertEquals(self.data, 'CONNECT: joe Cake Man {0}\r\n'.format(get_git_version()))

    def test_client_raises_exception_if_host_not_set(self):
        self.client.host = None
        self.assertRaises(Warning, self.client.connect, [None, None, 'sap saaap'])

    def test_da_ping_is_ponged(self):
        self.client.parser.parse('PING: 133337')
        self.data = self.con.recv(1024)
        self.assertEquals(self.data, 'PONG: 133337\r\n')

    def test_join_channel(self):
        self.client.parser.parse('JOIN: #Lobby')
        self.data = self.con.recv(1024)
        self.assertEquals(self.data, 'JOIN: #Lobby\r\n')

    def test_send_message(self):
        self.client.parser.parse('MSG #Lobby: WAZZAAAAAA?!')
        self.data = self.con.recv(1024)
        self.assertEquals(self.data, 'MSG #Lobby: WAZZAAAAAA?!\r\n')

    def test_send_talk(self):
        self.client.parser.parse('TALK John: Request')
        self.data = self.con.recv(1024)
        self.assertEquals(self.data, 'TALK John: Request\r\n')
        self.assertEquals(sys.stdout.getvalue().strip(), '[VoIP] Awaiting response from John...')

    def test_request_response_accept(self):
        self.cli.prompt_by_requester = 'John'
        voix.interface.cli.raw_input = lambda _: 'y'
        self.cli.main_loop()
        self.data = self.con.recv(1024)
        self.assertEquals(self.data, 'TALK John: Accept\r\n')

    def tearDown(self):
        self.client.close()
        self.server.close()



if __name__ == '__main__':
    unittest.main()
