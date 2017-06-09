# -*- coding: utf-8 -*-
import os

class Parseable(object):
    """The base class for element which can be parsed."""

    def __init__(self, file_name):
        self._file_name = file_name

    def is_existed(self):
        return os.path.exists(self._file_name)

    def parse_file(self):
        pass


