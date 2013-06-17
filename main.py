#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Start the client.

"""

import logging

from voix.client import Client


def main(detailed_logging = True):
    if detailed_logging:
        FORMAT = "%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s"
    else:
        FORMAT = "%(message)s"
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    client = Client()
    try:
        while True:
            action = raw_input()
            client.perform_action(action)
    except KeyboardInterrupt:
        client.close()
        print ""
        print "Shutting down..."

if __name__ == "__main__":
    main()
