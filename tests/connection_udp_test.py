#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import unittest
import mox
import random
import sys
import pyaudio
import wave
import time

from version import get_git_version
from voix.client import Client
from voix.connection import Connection
import voix.interface.cli
from voix.interface.cli import CLI


class ConnectionUDPTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.host = 'localhost'
        self.client.tcp.connected = True
        self.client.port = str(random.randint(9000, 12000))
        self.cli = CLI(self.client)
        self.cli.timeout = 2

        self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpsock.bind(('localhost', int(self.client.port)))
        self.tcpsock.listen(5)

        self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpsock.bind(('localhost', int(self.client.port) + 1))

        self.client.tcp.connect(('localhost', int(self.client.port)))
        self.tcpcon, addr = self.tcpsock.accept()

        wf = wave.open('assets/audio_test/noise.wav')
        self.data = wf.readframes(1024)[:1024]

    def test_stream_opened(self):
        self.client.udp.open_stream = lambda: self.assertTrue(True)
        self.client.parser.parse('TALK John: Accept')

    def test_stream_closed(self):
        self.client.udp.close_stream = lambda: self.assertTrue(True)
        self.client.parser.parse('TALK John: End')

    def test_udp_stream_server_to_client(self):
        self.client.parser.parse('TALK Dean John: Accept')
        self.udpsock.sendto(self.data, (self.client.host, self.client.udp.port))
        self.client.udp.output.write = lambda d: self.assertEquals(self.data, d)
        self.client.udp.in_handle.start()
        time.sleep(1)

    def test_udp_stream_client_to_server(self):
        self.client.parser.parse('TALK Sam: Accept')
        self.client.udp.input.read = lambda x: self.data
        self.client.udp.out_handle.start()
        time.sleep(1)
        data, addr = self.udpsock.recvfrom(1024)
        self.assertEquals(self.data, data)

    def tearDown(self):
        self.client.close()
        self.tcpsock.close()



if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s"
    )
    unittest.main()
