#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MessageHandler(object):
    def __init__(self):
        """
        SAP!

        """
        super(MessageHandler, self).__init__()
        self.talk = None

    def register_message_callback(self, func):
        """
        author,
        recipient,
        channel,
        message
        """
        self.message = func

    def register_talk_callback(self, func):
        """
        requester,
        responder
        """
        self.talk = func
