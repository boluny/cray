# -*- coding: utf-8 -*-
'''Module for basic class for all parseable content object'''

import codecs
import os
import io

from cray.craylib import utility

MY_LOGGER = utility.get_logger('cray.parseable')

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
            MY_LOGGER.warning("specified file %s does not exist.", self._file_name)
            return

        with codecs.open(self._file_name, 'r', 'utf-8') as parseable_fd:
            whole_content = parseable_fd.read()
            my_parser = Parser(whole_content)
            self.__meta, self.__content = my_parser.parse()

        MY_LOGGER.debug("meta: %s", self.__meta)
        MY_LOGGER.debug("content: %s", self.__content)

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

class Parser(object):
    """description of class"""
    def __init__(self, content):
        self.__content = content

    def parse(self):
        '''
        Parse the content of a parable object.
        :returns: --> tuple (meta, content)
        '''
        meta = dict()
        triple_hyphen = 0
        buf = io.StringIO(self.__content)

        # TODO: optimize the search of metadata start with and end with '---'
        # using regular expression
        line = buf.readline()
        while line is not None:
            if line.startswith('---'):
                triple_hyphen += 1

            if triple_hyphen == 1:
                if not line.startswith('-') and not line.startswith('#'):
                    # let maxsplit set to 1 to just take the first ':' as splitter
                    attribute_and_value = line.split(':', 1)
                    meta[attribute_and_value[0].strip()] = \
                        attribute_and_value[1].strip()
            elif triple_hyphen == 2:
                # if the second '---\n' is encountered, it means meta part is over
                break

            line = buf.readline()

        content = buf.read()

        return meta, content
