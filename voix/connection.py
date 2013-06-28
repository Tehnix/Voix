#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
import socket
import logging
import pyaudio
import random


class Connection(object):
    types = {'TCP': socket.SOCK_STREAM,
             'UDP': socket.SOCK_DGRAM}

    def __init__(self, client, type):
        super(Connection, self).__init__()
        self.sock = socket.socket(socket.AF_INET, Connection.types.get(type))
        self.client = client
        self.buf_size = 1024
        self.input = None
        self.output = None
        self.connected = None

        if type == 'UDP':
            self.in_handle = Thread(target=self.udp_in_handler)
            self.in_handle.daemon = True
            self.out_handle = Thread(target=self.udp_out_handler)
            self.out_handle.daemon = True
            self.audio = pyaudio.PyAudio()
            self.port = random.randint(9000, 12000)
        else:
            self.handle = Thread(target=self.tcp_handler)
            self.handle.daemon = True

    def connect(self, address):
        self.sock.connect(address)

    def send(self, data):
        self.sock.send(data)

    def tcp_handler(self):
        data = ''

        while True:
            try:
                data += self.sock.recv(self.buf_size)
            except socket.error:
                break

            if '\r\n' in data:
                self.client.parser.parse(data)
                data = ''

    def udp_in_handler(self):
        data = ''
        while True:
            try:
                data, addr = self.sock.recvfrom(self.buf_size)
            except socket.error:
                break
            self.output.write(data)

    def udp_out_handler(self):
        data = ''
        while True:
            data = self.input.read(1024)
            try:
                self.sock.sendto(
                    data,
                    (self.client.host, int(self.client.port) + 1)
                )
            except socket.error:
                break

    def is_connected(self):
        return self.connected

    def open_stream(self):
        """
        Opens a UDP stream to the server, which redirects the
        traffic to the connected clients.

        """
        self.sock.bind((self.client.host, self.client.udp.port))
        self.output = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=10240,
                                      output=True)
        self.input = self.audio.open(format=pyaudio.paInt16,
                                     channels=1,
                                     rate=10240,
                                     input=True,
                                     frames_per_buffer=1024)

    def close_stream(self):
        """
        Opens a UDP stream to the server, which redirects the
        traffic to the connected clients.

        """
        self.sock.close()
        self.input.close()
        self.output.close()

    def close(self):
        """Wrapper for the sockets close function."""
        if self.sock:
            return self.sock.close()
        else:
            return
