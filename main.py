#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Start the client.

"""

import logging
import argparse
import wx

from voix.client import Client
from voix.interface.cli import CLI
from voix.interface.gui import GUI


parser = argparse.ArgumentParser(
    description='A voice communication and chat client.'
)
parser.add_argument(
    '-v',
    '--verbose',
    dest='verbose',
    action='store_true',
    help='prints detailed steps to stdout.'
)
parser.add_argument(
    '-c',
    '--cli',
    dest='cli',
    action='store_true',
    help='uses CLI instead of GUI.'
)

options = parser.parse_args()

def main():
    if options.verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s"
        )

    client = Client()

    if options.cli:
        cli = CLI(client)
        cli.main_loop()
    else:
        app = wx.App()
        GUI(None, -1, 'Voix')
        app.MainLoop()


if __name__ == "__main__":
    main()
