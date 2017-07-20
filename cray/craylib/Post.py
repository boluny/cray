# -*- coding: utf-8 -*-
'''
The module of a post object.
'''

from cray.craylib.parse import Parseable


class Post(Parseable):
    """A representation of a post of a blog. """
    def __init__(self, file_name):
        '''Create a post object with absolute file name. '''
        super().__init__(file_name)
