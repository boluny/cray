# -*- coding: utf-8 -*-
from craylib import utility
from craylib.Parser import Parser
import os
import codecs

_logger = utility.get_logger('cray.post')

class Post(object):
    """description of class"""
    def __init__(self, filename):
        self._post_meta_data = {}
        self._post_content = ""
        self._post_file_name = filename
        _logger.debug("receive file name: " + filename)

    def get_content(self):
        return self._post_content

    def get_metadata(self):
        return self._post_meta_data

    def parse_file(self):

        # TODO: add exception or failture test
        if not self.is_existed():
            _logger.warning("specified file %s does not exist.", self._post_file_name)
            return

        # TODO: handle different file encoding
        with codecs.open(self._post_file_name, 'r', 'utf-8') as post_fd:
            whole_content = post_fd.read()
            pp = Parser(whole_content)
            self._post_meta_data, self._post_content = pp.parse()

        _logger.debug("meta: %s", self._post_meta_data)
        _logger.debug("content: %s", self._post_content)
        return utility.RT.SUCCESS

    def is_existed(self):
        return os.path.exists(self._post_file_name)
