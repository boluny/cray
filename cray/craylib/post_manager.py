# -*- coding: utf-8 -*-
'''module for post management class'''

import os
import textwrap
from datetime import datetime, date
from cray.craylib import post, utility

#from .Post import *

_LOGGER = utility.get_logger('cray.PostManager')

class PostManager(object):
    """The class to manage all the posts in the sites."""
    def __init__(self, post_dir):
        self.__post_dir = post_dir
        self.__posts_list = []
        _LOGGER.debug('post_dir: %s', post_dir)

    def parse_arg(self, params):
        """
        Execute for the specified command e.g. new/list
        :param params: The command argument after subcommand 'post'
        :returns: None
        """

        _LOGGER.debug('params: %s', params)

        if params.command_name == 'list':
            self.__posts_list = self.list_all_post()
            print(*self.__posts_list, sep='\n')
            exit(0)
            # For other command extension with one parameter

        if params.command_name == 'read':
            meta, content = self.read_post(params.file_name)
            if params.meta:
                print(meta)
            elif params.content:
                print(content)
            else:
                print(meta)
                print(content)
        elif params.command_name == 'create':
            # file name goes like hello-world.md
            self.create(params.file_name)
        elif params.command_name == 'delete':
            self.delete(params.file_name)

    def list_all_post(self):
        '''print all files under _post dir'''
        return os.listdir(self.__post_dir)

    def read_post(self, file_name):
        '''read specified post meta and content
        :param file_name: specified file name
        :type file_name: str
        :returns: (meta, content)
        :rtype: tuple (list, str)
        '''
        this_post = post.Post(os.path.join(self.__post_dir, file_name))
        ret_list = [{}, '']
        if this_post.parse_file() == utility.RT.SUCCESS:
            ret_list[0] = this_post.get_meta()
            ret_list[1] = this_post.get_content()
        else:
            print("error when parsing post", file_name)

        return tuple(ret_list)

    def create(self, file_name):
        '''Create the target file'''
        file_name_words = os.path.splitext(file_name)[0].split('-')
        file_name_with_date = str(date.today()) + '-' + file_name
        full_path = os.path.join(self.__post_dir, file_name_with_date)

        if os.path.exists(full_path):
            print("Error: same post file exists!")
            exit(-1)

        content = \
'''---
layout: post
title: "%s"
date: %s +0800
---

content goes here
'''
        # date e.g. 2015-09-22 11:09:00
        with open(full_path, 'w', encoding='utf-8') as post_fd:
            post_fd.write(textwrap.dedent(content) % \
            (' '.join(file_name_words), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        print("Successfully create post", file_name_with_date)

    def delete(self, file_name):
        '''delete the specified file
        file_name: the file name which is desired to be deleted
        '''
        file_abs_path = os.path.join(self.__post_dir, file_name)
        if not os.path.exists(file_abs_path):
            print('Error: post', file_name, 'does not exist in post dir!')
            exit(-1)
        if not os.path.isfile(file_abs_path):
            print('Error: post', file_name, 'point to a directory')
            exit(-1)

        # TODO: add an dialog to ask for confirming
        os.remove(file_abs_path)
        print('Successfully remove post', file_name)

    def get_all_posts(self):
        '''
        Get all the posts' content including meta and content.
        :returns: -> list
        '''
        post_list = []
        files = os.listdir(self.__post_dir)
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                _post = post.Post(os.path.join(self.__post_dir, file))
                if _post.parse_file() == utility.RT.SUCCESS:
                    post_list.append(_post)

        return post_list
