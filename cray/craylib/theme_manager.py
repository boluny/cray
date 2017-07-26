# -*- coding: utf-8 -*-
'''module mainly for theme management class'''

import os

class ThemeManager(object):
    """manager of themes"""

    def __init__(self, theme_dir):
        self.__theme_dir = theme_dir
        self.__theme = []
        self.__theme_name = ""
        self.__tpl_index = ""
        self.__tpl_post = ""
        self.__tpl_page = ""

    def set_theme(self, theme_name):
        '''
        Specified the theme that used for rendering the site.
        :param theme_name: the name of the subdirectory in the _theme directory.
        :returns: --> None
        '''
        self.__theme_name = theme_name
        self.__tpl_index = os.path.join(self.__theme_dir, self.__theme_name, "index.html")
        self.__tpl_post = os.path.join(self.__theme_dir, self.__theme_name, "post.html")
        self.__tpl_page = os.path.join(self.__theme_dir, self.__theme_name, "page.html")

    def is_theme_usable(self):
        '''
        Check if the theme has the necessary template file: index.html, post.html and page.html.
        :returns: --> bool
        '''
        if os.path.exists(self.__tpl_index) \
            and os.path.exists(self.__tpl_page) \
            and os.path.exists(self.__tpl_post):
            return True

        return False

    def get_current_theme(self):
        '''
        Get the current used theme.
        :return: --> str
        '''
        return self.__theme_name

    def get_template_path(self):
        '''
        get the absolute path of three mainly template: index, post and page.
        :returns: --> dict(index=..., post=..., page=...)
        '''
        if not self.is_theme_usable():
            return None

        return dict(index=self.__tpl_index, post=self.__tpl_post, page=self.__tpl_page)

    def get_abs_path(self):
        '''
        get the absolute path of the specified set theme.
        :returns: --> str
        '''
        return os.path.join(self.__theme_dir, self.__theme_name)
