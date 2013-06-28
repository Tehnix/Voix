#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from wx import Frame


class GUI(Frame):
    def __init__(self, parent, id, title):
        """Initializes the GUI

        Arguments:
        - `self`:
        - `parent`:
        - `id`:
        - `title`:
        """
        super(GUI, self).__init__(parent, id, title, size=(340, 380))
        self.Centre()
        self.Show(True)
