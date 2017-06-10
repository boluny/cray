# -*- coding: utf-8 -*-
'''Module for basic class for all parseable content object'''

import codecs
import os

from craylib import utility
from craylib.Parser import Parser

module_logger = utility.get_logger('cray.parseable')

class Parseable(object):
    """The base class for element which can be parsed."""

    def __init__(self, file_name):
        self._file_name = file_name
        self.__hooker_func = None
        self.__meta = {}
        self._post_process_meta = {}
        self.__content = ""

    def is_existed(self):
        '''Check if file existed in the intialized path'''
        return os.path.exists(self._file_name)

    def parse_file(self):
        '''
        Parse the file which in following format:
        ---
        meta_key: meta_value
        ...
        ---

        content
        '''
        # TODO: add exception or failture test
        if not self.is_existed():
            module_logger.warning("specified file %s does not exist.", self._file_name)
            return

        with codecs.open(self._file_name, 'r', 'utf-8') as parseable_fd:
            whole_content = parseable_fd.read()
            my_parser = Parser(whole_content)
            self.__meta, self.__content = my_parser.parse()

        module_logger.debug("meta: %s", self.__meta)
        module_logger.debug("content: %s", self.__content)

        if self.__hooker_func and callable(self.__hooker_func):
            self.__hooker_func(self.__meta)

        return utility.RT.SUCCESS

    def get_meta(self):
        '''
        Return the metadata of the parsable object.
        '''
        return self.__meta

    def get_content(self):
        '''
        Return the content of the parsable object.
        '''
        return self.__content

    def set_post_process_hook(self, hooker=None):
        '''
        Set hooker function to do post process after parse the object.
        '''
        self.__hooker_func = hooker
