# -*- coding: utf-8 -*-
'''module for site creation class'''

import os
import textwrap
from datetime import date

class CreateManager(object):

    def __init__(self, cur_dir, site_name):
        '''
        A creator manager responsible to create new site
        maybe builder pattern is better?
        '''
        # TODO: Validate the passed in site name does not have illegal characters
        self.__site_root = os.path.join(cur_dir, site_name)

    def create(self):
        '''the public interface to create the site'''
        if self.check_site_exist():
            return False

        self._create_posts()
        self.create_pages()
        self.create_themes()
        self.create_config_file()
        return True

    def _create_posts(self):
        post_dir = os.path.join(self.__site_root, '_post')
        os.makedirs(post_dir, 0o777, True)
        
        file_name = str(date.today()) + '-hello-world.md'
        content = '''
---
layout: post
title: "hello world!"
categories: test
type: tech
date: 2015-09-22 11:09:00 +0800
---
hello world

it's a code snippet:

    int foo(int bar)
    {
        return 0;
    }

'''
        with open(os.path.join(post_dir, file_name), 'w', encoding='utf-8') as hello_fd:
            hello_fd.write(textwrap.dedent(content))
        
        return True

    def create_pages(self):
        post_dir = os.path.join(self.__site_root, '_page')
        os.makedirs(post_dir, 0o777, True)
        
        file_name = 'about.md'
        content = '''
---
layout: page
title: 关于
permalink: /about/
---
demo `about` page

'''
        with open(os.path.join(post_dir, file_name), 'w', encoding='utf-8') as about_fd:
            about_fd.write(content)
        
        return True

    def create_themes(self):
        default_theme_dir = os.path.join(self.__site_root, '_theme', 'simple')
        os.makedirs(default_theme_dir, 0o777, True)

        file_list = [
            ('footer.html',
            '''
<footer>
<h3>Powered by Cray 2017</h3>
</footer>
            '''),
            ('header.html',
            '''
<header class="site-header">
  <div class="wrapper">
    <a class="site-title" href="/">Index</a>
    <nav class="site-nav">
      <div class="trigger">
        {% for page in site.pages %}
          {% if page.title %}
          <a class="page-link" href="{{ page.url }}">{{ page.title }}</a>
          {% endif %}
        {% endfor %}
      </div>
    </nav>
  </div>
</header>
            '''),
            ('index.html',
            '''
<html>
<head>
	<meta charset="utf-8">
    <title>Index</title>
</head>
<body>
	{% include 'header.html' %}
	<h1>Post list:</h1>
    <ul id="navigation">
    {% for post in posts %}
        <li><a href="{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
    </ul>

    {% include 'footer.html' %}
</body>
</html>
            '''),
            ('page.html',
            '''
<html>
<head>
	<meta charset="utf-8">
    <title>{{ page.title }}</title>
</head>
<body>
	{% include 'header.html' %} 
	<h1>{{ page.title }}</h1>
	<div>{{ page.content }}</div>
	
	{% include 'footer.html' %} 
    
</body>
</html>
            '''),
            ('post.html',
            '''
<html>
<head>
	<meta charset="utf-8">
    <title>{{ post.title }}</title>
</head>
<body>
	{% include 'header.html' %} 
	<h1>{{ post.title }}</h1>
	<p>{{ post.date }}</p>
	<div>{{ post.content }}</div>
	
	{% include 'footer.html' %} 
    
</body>
</html>
            ''')
        ]
        for file_name, content in file_list:
            with open(os.path.join(default_theme_dir, file_name), 'w') as _fd:
                _fd.write(textwrap.dedent(content))           


    def create_config_file(self):
        config_content='''
{
    "title": "Demo",
    "description": "demo site description",
    "url": "http://www.demo.com",
    "generate_path": "..",
    "theme":"simple"
}        
        '''
        with open(os.path.join(self.__site_root, 'config.json'), 'w') as config_fd:
            config_fd.write(config_content)
        

    def check_site_exist(self):
        return os.path.exists(self.__site_root)
