# -*- coding: utf-8 -*-
import os
import shutil
import codecs
import markdown
from datetime import datetime
from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from craylib.ThemeManager import ThemeManager
from craylib.PostManager import PostManager
from craylib.PageManager import PageManager
from craylib import utility


_logger = utility.get_logger('cray.GenerateManager')

class GenerateManager(object):
    """Response to generate the static site"""

    def __init__(self, root_dir):
        self._root_dir = root_dir
        self.__default_file_name = "index.html"
        self.__site_dict = {}       

    def set_tar_dir(self, tar_dir):
        self._tar_dir = tar_dir
        self._abs_dir = os.path.join(self._root_dir, self._tar_dir)

    def set_theme_dir(self, theme_dir):
        self._theme_dir = theme_dir

    def set_post_dir(self, post_dir):
        self._post_dir = post_dir

    def set_page_dir(self, page_dir):
        self._page_dir = page_dir

    def __check_validation(self):
        return os.path.exists(self._abs_dir)

    def __clear_site(self):
        if self.__check_validation():
            shutil.rmtree(self._abs_dir, ignore_errors=True)

    def generate_site(self):
        if self.__check_validation():
            self.__clear_site()

        # main logic:
        # 1.  read theme template
        # 2.  parge posts and pages and save to dict
        # 3.  couple the generated dict with readed templates

        if not hasattr(self, '_theme_dir'):
            _logger.error("no theme directory")
            return

        tm = ThemeManager(self._theme_dir)
        tm.set_theme('')
        site_template_path = tm.get_template_path()

        if not hasattr(self, '_page_dir'):
            _logger.error("no page directory")
            return

        page_manager = PageManager(self._page_dir)
        pages = page_manager.get_all_pages()
        self.__site_dict['pages'] = pages

        if not hasattr(self, '_post_dir'):
            _logger.error("no post directory")
            return

        pm = PostManager(self._post_dir)
        posts = pm.get_all_posts()

        if site_template_path is not None:
            self.generate_pages(site_template_path['page'])
            posts_meta = self.generate_posts(site_template_path['post'], posts)
            self.generate_index(site_template_path['index'], posts_meta)
            
    def generate_posts(self, post_template_path, posts):
        if len(posts) == 0 or post_template_path == '':
            return []

        posts_meta = []
        for post in posts:
            per_meta = {}
            # Delegate the metadata from post itself to the tempoary containers
            # for generator global usage
            # TODO: make it a class member?
            for k, v in post.get_metadata().items():
                per_meta[k] = v
            
            # trim post.title to get rid of double quotation mark
            if 'title' in per_meta:
                per_meta['title'] = utility.trim_quotation_mark(per_meta['title'])

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
                    '-'.join(str(x) for x in [pd.hour,'placeholder']))
                url = os.path.join(url_dir, self.__default_file_name)
                os.makedirs(os.path.join(self._abs_dir, url_dir))
                file_path = os.path.join(self._abs_dir, url)

                result = self.__template_helper(post_template_path, post=per_meta, site=self.__site_dict)
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
            # TODO: markdown parse
            page_content = markdown.markdown(page['content'])

            url_dir = page['url_dir']
            url = os.path.join(url_dir, self.__default_file_name)
            os.makedirs(os.path.join(self._abs_dir, url_dir))
            file_path = os.path.join(self._abs_dir, url)

            result = self.__template_helper(page_template_path, page=page, site=self.__site_dict)
            with codecs.open(file_path, 'w', 'utf-8') as post_fd:
                post_fd.write(result)


    def generate_index(self, index_template_path, posts_meta):
        file_path = os.path.join(self._abs_dir, self.__default_file_name)
        result = self.__template_helper(index_template_path, posts=posts_meta, site=self.__site_dict)

        with codecs.open(file_path, 'w', 'utf-8') as index_fd:
            index_fd.write(result)
    
    def __template_helper(self, template_path, **kwargs):
        env = Environment()
        template_dir, template_name = os.path.split(template_path)
        env.loader = FileSystemLoader(template_dir)
        template = env.get_template(template_name)
        result = template.render(kwargs)

        return result
        




