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
            '{0} wish to have a conversation with you. Accept? (y/n)',
            'Awaiting response from {0}...',
            '{0} has rejected your conversation request.',
            'Your conversation with {0} has been terminated.'
        ]

        message = None
        if requester and code.lower() == 'request':
            message = msgs[0].format(requester)

        if not message is None:
            self.prompt_by_requester = requester

        if not requester and code.lower() == 'request':
            message = msgs[1].format(responder)

        if not message is None:
            t = Timer(self.timeout, self.talk_timeout_timer)
            t.start()

        if not requester and code.lower() == 'deny':
            message = msgs[2].format(responder)

        if requester and code.lower() == 'end':
            message = msgs[3].format(requester)

        if not requester and code.lower() == 'end':
            message = msgs[3].format(responder)

        print '[VoIP] %s' % message

    def talk_timeout_timer(self):
        self.prompt_by_requester = None
        print '[VoIP] Request timed out!'

    def main_loop(self):
        """
        """
        try:
            while True:
                action = raw_input()

                req = self.prompt_by_requester
                if req:
                    if action == 'y':
                        action = 'Accept'
                    elif action == 'n':
                        action = 'Deny'
                    action = 'TALK {0}: %s'.format(req) % action
                    self.prompt_by_requester = None

                self.client.parser.parse(action)

                if self._testing:
                    break
        except KeyboardInterrupt:
            self.client.close()
            print ""
            print "Shutting down..."
