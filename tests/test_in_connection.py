#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import unittest
import mox
import random
import sys
import time
from io import StringIO

from version import get_git_version
from voix.client import Client
from voix.connection import Connection
from voix.interface.cli import CLI

class ConnectionInTest(unittest.TestCase):
    def setUp(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = Client()
        self.cli = CLI(self.client)
        self.client.port = str(random.randint(9000, 12000))
        self.server.bind(('localhost', int(self.client.port)))
        self.server.listen(5)
        self.client.tcp.connected = True

        self.client.nick = 'John'
        self.client.tcp.connect(('localhost', int(self.client.port)))
        self.con, addr = self.server.accept()
        self.client.tcp.send(bytes('CONNECT: John Cake Man 1.0.0\r\n'))
        self.data = self.con.recv(1024)

    def test_receive_message_author_chan(self):
        self.con.send(bytes('MSG Tehnix #Lobby: <(^.^<)\r\n'))
        self.client.tcp.handle.start()
        time.sleep(1)
        self.assertEquals(sys.stdout.getvalue().strip(), '[#Lobby] Tehnix: <(^.^<)')

    def test_receive_message_author_recipient(self):
        self.con.send(bytes('MSG Tehnix JLow: <(^.^<)\r\n'))
        self.client.tcp.handle.start()
        time.sleep(1)
        self.assertEquals(sys.stdout.getvalue().strip(), '[PM: JLow] Tehnix: <(^.^<)')

    def tearDown(self):
        self.client.close()
        self.server.close()


if __name__ == '__main__':
    unittest.main()
