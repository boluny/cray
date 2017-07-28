# -*- coding: utf-8 -*-
'''
The module of a post manager object.
'''
import os

from cray.craylib import utility
from cray.craylib.page import Page

_LOGGER = utility.get_logger('cray.PageManager')

class PageManager(object):
    """Manager of pages"""
    _init_template = ""

    def __init__(self, page_dir):
        self.__cmd_params = 'transient'
        self.__page_dir = page_dir
        _LOGGER.debug('page_dir: %s', page_dir)

    def create(self, file_name):
        '''
        Generate a new page file with specified name.
        :param file_name: the name for the page file, default also set to page title.
        :returns: --> bool
        '''
        pass

    def delete(self, file_name):
        '''
        Delete a new page file with specified name.
        :param file_name: the name for the page file to be deleted.
        :returns: --> bool
        '''
        pass

    def is_exist(self, file_name):
        '''
        Check if the specified page file exists.
        :param file_name: the name for the page file to be checked.
        :returns: --> bool
        '''
        pass

    def get_all_pages(self):
        '''
        Get all the pages in a list of page objects.
        :returns: --> list
        '''
        page_list = []
        files = os.listdir(self.__page_dir)
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                one_post = Page(os.path.join(self.__page_dir, file))
                if one_post.parse_file() == utility.RT.SUCCESS:
                    page_list.append(one_post.as_dict())

        return page_list

    def get_page_names(self):
        '''
        Get all the pages file names without extension and without path.
        :returns: --> list
        '''
        files = os.listdir(self.__page_dir)
        return map(utility.file_name_no_ext, files)
