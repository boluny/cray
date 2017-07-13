# -*- coding: utf-8 -*-
'''module for post management class'''

import os
import textwrap
from datetime import datetime, date
from cray.craylib import Post, utility

#from .Post import *

_logger = utility.get_logger('cray.PostManager')

class PostManager(object):
    """The class to manage all the posts in the sites."""
    def __init__(self, post_dir):
        self.__post_dir = post_dir
        self.__posts_list = []
        _logger.debug('post_dir: %s', post_dir)

    def parse_arg(self, params):
        """
        Execute for the specified command e.g. new/list
        """

        self.__params = params
        _logger.debug('params: %s', params)

        if len(self.__params) == 1:
            if self.__params[0] == 'list':
                self.list_all_post()
                exit(0)
            # For other command extension with one parameter

        assert len(self.__params) == 2
        if self.__params[0] == 'read':
            pp = Post.Post(os.path.join(self.__post_dir, self.__params[1]))
            if pp.parse_file() == utility.RT.SUCCESS:
                print(pp.get_meta())
                print(pp.get_content())
        elif self.__params[0] == 'create':
            # file name goes like hello-world.md
            self.create(self.__params[1])
        elif self.__params[0] == 'delete':
            self.delete(self.__params[1])

    def list_all_post(self):
        '''print all files under _post dir'''
        print(*os.listdir(self.__post_dir), sep='\n')

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
        with open(full_path, 'w', encoding='utf-8') as fd:
            fd.write(textwrap.dedent(content) % \
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

    def is_post_exist(self, file_name):
        pass

    def set_post_dir(self, path):
        pass

    def get_all_posts(self):
        post_list = []
        files = os.listdir(self.__post_dir)
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                pp = Post.Post(os.path.join(self.__post_dir, file))
                if pp.parse_file() == utility.RT.SUCCESS:
                    post_list.append(pp)

        return post_list
