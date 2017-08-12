# -*- coding: utf-8 -*-
'''
The module of a post object.
'''

from cray.craylib.parse import Parseable
from cray.craylib import utility


class Post(Parseable):
    """A representation of a post of a blog post. """
    def __init__(self, file_name):
        '''Create a post object with absolute file name. '''
        self.__file_name = file_name
        super().__init__(file_name)
        self.set_post_process_hook(self.post_post_process)

    def post_post_process(self, fresh_meta):
        '''customized post process logic for post object'''
        # Imagine that file name format like yyyy-mm-dd-title.md
        fresh_meta['__file_name'] = utility.file_name_no_ext(self.__file_name)[11:].split('-')
