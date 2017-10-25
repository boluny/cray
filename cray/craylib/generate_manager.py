# -*- coding: utf-8 -*-
'''module for site generation class'''

import codecs
import os
import shutil
from datetime import datetime

import markdown
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

from cray.craylib import utility
from cray.craylib.page_manager import PageManager
from cray.craylib.post_manager import PostManager
from cray.craylib.theme_manager import ThemeManager

_logger = utility.get_logger('cray.GenerateManager')

class GenerateManager(object):
    """Response to generate the static site"""

    def __init__(self, root_dir):
        self._root_dir = root_dir
        self.__default_file_name = "index.html"
        self.__site_dict = {}
        self._abs_dir = ""
        self._theme_dir = ""
        self._post_dir = ""
        self._page_dir = ""

    def set_tar_dir(self, tar_dir):
        self._abs_dir = tar_dir

    def set_theme_dir(self, theme_dir):
        self._theme_dir = theme_dir

    def set_post_dir(self, post_dir):
        self._post_dir = post_dir

    def set_page_dir(self, page_dir):
        self._page_dir = page_dir

    def __check_validation(self):
        #print(self._abs_dir, "exists.")
        return os.path.exists(self._abs_dir)

    def __clear_site(self):
        if self.__check_validation():
            shutil.rmtree(self._abs_dir, ignore_errors=True)

    def generate_site(self):
        '''The main function to generate the whole site'''
        if 'generate_path' not in self.__site_dict:
            _logger.info("Not specify the generate path, please check carefully")

        if 'theme' not in self.__site_dict:
            _logger.error("Theme is not specified, please check carefully")
            return

        theme_subdir = self.__site_dict if 'include_theme_subdir' in self.__site_dict \
        else ["js", "css", "image"]
        self.set_theme_dir(os.path.join(self._root_dir, utility.THEME_DIR))
        self.set_post_dir(os.path.join(self._root_dir, utility.POST_DIR))
        self.set_page_dir(os.path.join(self._root_dir, utility.PAGE_DIR))
        self.set_tar_dir(utility.full_generate_path(self._root_dir, self.__site_dict))

        # main logic:
        # 1.  read theme template
        # 2.  parge posts and pages and save to dict
        # 3.  couple the generated dict with readed templates

        if not self._theme_dir:
            _logger.error("no theme directory")
            return

        tm = ThemeManager(self._theme_dir)
        tm.set_theme(self.__site_dict['theme'])
        site_template_path = tm.get_template_path()

        if not self._page_dir:
            _logger.error("no page directory")
            return

        if not self._post_dir:
            _logger.error("no post directory")
            return

        page_manager = PageManager(self._page_dir)
        pages = page_manager.get_all_pages()

        if utility.name_conflict(page_manager.get_page_names(), theme_subdir):
            _logger.error("page name conflict with configured included theme subdirectories.")
            return

        self.__site_dict['pages'] = pages

        pm = PostManager(self._post_dir)
        posts = pm.get_all_posts()

        if site_template_path is not None:
            # TODO: any error after clear the site is disallowed,
            # so careful check should be done before this segment
            if self.__check_validation():
                self.__clear_site()
            self.generate_pages(site_template_path['page'])
            posts_meta = self.generate_posts(site_template_path['post'], posts)
            self.generate_index(site_template_path['index'], posts_meta)
            utility.copy_subdir(tm.get_abs_path(), theme_subdir, self._abs_dir)
            print("Site generation is finished!")

    def read_config(self, config_loader):
        self.__site_dict.update(config_loader.get_config())
        return True

    def generate_posts(self, post_template_path, posts):
        """
        Generate post HTML pages using the passed in template and posts sequence.\n
        post_template_path|str: the template path\n
        posts|list: post sequence which contains all posts metadata and content\n
        """
        # use `not posts` rather than `len(posts)` to match PEP8
        if not posts or post_template_path == '':
            return []

        posts_meta = []
        for post in posts:
            per_meta = {}
            # Delegate the metadata from post itself to the tempoary containers
            # for generator global usage
            # TODO: make it a class member?
            for k, v in post.get_meta().items():
                per_meta[k] = v

            # trim post.title to get rid of double quotation mark
            if 'title' in per_meta:
                per_meta['title'] = utility.trim_double_quotation_mark(per_meta['title'])

            # TODO: markdown parse
            per_meta['content'] = markdown.markdown(post.get_content())
            if 'date' in per_meta:
                # TODO: which is more efficient?  regexp before or try...catch
                # block
                try:
                    pd = datetime.strptime(per_meta['date'], '%Y-%m-%d %H:%M:%S %z')
                except ValueError:
                    pd = datetime.strptime(per_meta['date'], '%Y-%m-%d %H:%M:%S')

                url_dir = os.path.join('post', str(pd.year), str(pd.month), str(pd.day), \
                    '-'.join(str(x) for x in per_meta['__file_name']))
                url = os.path.join(url_dir, self.__default_file_name)
                os.makedirs(os.path.join(self._abs_dir, url_dir))
                file_path = os.path.join(self._abs_dir, url)

                result = self.__template_helper(post_template_path, \
                post=per_meta, site=self.__site_dict)
                with codecs.open(file_path, 'w', 'utf-8') as post_fd:
                    post_fd.write(result)

                per_meta['url'] = url_dir
                posts_meta.append(per_meta)
            else:
                _logger.warning("Cannot find date information for post %s", per_meta['title'])

        return posts_meta

    def generate_pages(self, page_template_path):
        if len(self.__site_dict['pages']) == 0 or page_template_path == '':
            return []

        for page in self.__site_dict['pages']:
            # TODO: markdown parser add TOC support
            page_content = markdown.markdown(page['content'])
            page['content'] = page_content

            url_dir = page['url_dir']
            url = os.path.join(url_dir, self.__default_file_name)
            os.makedirs(os.path.join(self._abs_dir, url_dir))
            file_path = os.path.join(self._abs_dir, url)

            result = self.__template_helper(page_template_path, page=page, site=self.__site_dict)
            with codecs.open(file_path, 'w', 'utf-8') as post_fd:
                post_fd.write(result)


    def generate_index(self, index_template_path, posts_meta):
        file_path = os.path.join(self._abs_dir, self.__default_file_name)
        result = self.__template_helper(index_template_path, posts=posts_meta, \
        site=self.__site_dict)

        with codecs.open(file_path, 'w', 'utf-8') as index_fd:
            index_fd.write(result)

    def __template_helper(self, template_path, **kwargs):
        env = Environment()
        env.filters['date'] = utility.jinja_datetime_format
        template_dir, template_name = os.path.split(template_path)
        env.loader = FileSystemLoader(template_dir)
        template = env.get_template(template_name)
        result = template.render(kwargs)

        return result
