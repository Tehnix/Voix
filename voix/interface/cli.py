#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import logging
import sys
from threading import Timer


class CLI(object):
    """
    """

    def __init__(self, client):
        """
        """
        super(CLI, self).__init__()
        client.register_update_callback(self.update)
        client.message_handler.register_message_callback(self.write_message)
        client.message_handler.register_talk_callback(self.talk_prompt)
        self.client = client
        self.timeout = 15
        self.prompt_by_requester = None
        self._testing = None

    def update(self, channel=None, userlist=None):
        """
        """

        message = ''
        if channel and not userlist:
            message = '[Joined] %s' % channel

        if userlist:
            message = '[{0}] Users: {1}'.format(channel, userlist)

        message = message.replace('\r\n', '')

        print message

    def write_message(self,
                      author=None,
                      recipient=None,
                      channel=None,
                      message=None):
        """

        Arguments:
        - `message`:
        """

        author = author is None and self.client.nick or author
        channel = not channel is None and '[%s] ' % channel or ''
        recipient = not recipient is None and '[PM: %s] ' % recipient or ''

        message = message.replace('\r\n', '')

        print '{0}{1}{2}: {3}'.format(channel, recipient, author, message)

    def talk_prompt(self, requester=None, responder=None, code=None):
        """
        Handles all `TALK` related requests and responses.

        Arguments:
        - `message`:
        [VoIP] `requester` wish to have a conversation with you. Accept? (y/n)
        [VoIP] Awaiting response from `responder`...
        [VoIP] `responder` has rejected your conversation request.
        [VoIP] Your conversation with `responder` has been terminated.
        """
        msgs = [
            '{0} wish to have a conversation with you. Accept? (y/n)', # TALK target 123: REQUEST
            'Awaiting response from {0}...', # TALK source 123: REQUEST
            'Conversation is now active.', # TALK !source-gem! 123: DENIED
            '{0} has rejected your conversation request.', # TALK !source-gem! 123: DENIED
            'Your conversation with {0} has been terminated.'
        ]

        message = None
        if requester and code == 'REQUEST':
            message = msgs[0].format(requester)
            self.requester = requester
            t = Timer(self.timeout, self.talk_timeout_timer)
            t.start()
        elif responder and code == 'REQUEST':
            message = msgs[1].format(responder)
            self.responder = responder
            t = Timer(self.timeout, self.talk_timeout_timer)
            t.start()
        elif code == 'ACCEPTED':
            message = msgs[2]
            self.responder = None
        elif code == 'DENIED':
            message = msgs[3].format(self.responder)


        if requester and code == 'END':
            message = msgs[3].format(requester)

        if not requester and code == 'END':
            message = msgs[3].format(responder)

        print '[VoIP] %s' % message

    def talk_timeout_timer(self):
        if self.requester or self.responder:
            print '[VoIP] Request timed out!'
            self.requester = None
            self.responder = None

    def main_loop(self):
        """
        """
        try:
            while True:
                action = raw_input()

                req = self.requester
                if req:
                    code = ''
                    if action == 'y':
                        code = 'ACCEPT'
                    else:
                        code = 'DENY'
                    action = 'TALK %s: %s' (self.client.udp.session_key, code)
                    self.requester = None

                self.client.parser.parse(action)

                if self._testing:
                    break
        except KeyboardInterrupt:
            self.client.close()
            print ""
            print "Shutting down..."
