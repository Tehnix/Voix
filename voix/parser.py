#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging


class Parser(object):
    def __init__(self, client):
        self.actions = {'HOST': client.set_host,
                        'PORT': client.set_port,
                        'CONNECT': client.connect,
                        'JOIN': client.join_channel,
                        'MSG': client.message,
                        'TALK': client.talk,
                        'ACCEPTED': client.accepted,
                        'NOTACCEPTED': client.denied,
                        'PING': client.pong,
                        'JOINED': client.joined_channel,
                        'USERLIST': client.userlist}

    def parse(self, data):
        """

        Arguments:
        - `self`:
        - `data`:
        """
        match = re.match(
            r'^([A-Z]+)[ ]?([0-9a-zA-Z]+)?[ ]?([0-9a-zA-Z#]+)?: (.+)$',
            data,
            re.DOTALL)
        if not match is None:
            groups = match.groups()
            func = self.actions.get(groups[0])
            try:
                func(groups[1:])
            except Warning as warn:
                logging.warning(warn)
