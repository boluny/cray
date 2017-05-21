from sys import argv
from jinja2 import Template
from craylib.PostManager import PostManager
from craylib.GenerateManager import GenerateManager
from craylib.utility import start_server

import os

TEST_SITE = 'sample_site'
POST_DIR = '_post'
PAGE_DIR = '_page'
THEME_DIR = '_theme'
GENERATED_SITE_DIR = '_site'

def usage():
    pass

if __name__ == '__main__':
    if len(argv) < 2:
        print("Arguments are not sufficient")
        usage()
        exit(-1)

    print(argv)
    print(os.path.join(os.getcwd(), TEST_SITE, POST_DIR))

    # handle post related command logic
    if argv[1] == 'post':

        posts_dir = os.path.join(os.getcwd(), TEST_SITE, POST_DIR)
        pm = PostManager(posts_dir)
        pm.execute(argv[2:])
        
    elif argv[1] == 'page':
        pass
    elif len(argv) == 2 and argv[1] == 'generate':
        gm = GenerateManager(os.path.join(os.getcwd(), TEST_SITE))
        gm.set_tar_dir(GENERATED_SITE_DIR)
        themes_dir = os.path.join(os.getcwd(), TEST_SITE, THEME_DIR)
        gm.set_theme_dir(themes_dir)
        gm.set_post_dir(os.path.join(os.getcwd(), TEST_SITE, POST_DIR))
        gm.set_page_dir(os.path.join(os.getcwd(), TEST_SITE, PAGE_DIR))
        gm.generate_site()      
    elif argv[1] == 'preview':
        # call HTTP module to start a server on the site directory
        # python -m http.server 8000
        site_dir = os.path.join(os.getcwd(), TEST_SITE, GENERATED_SITE_DIR)
        start_server(site_dir)
        
    elif argv[1] == 'deploy':
        pass
    else:
        print("Unimplemented option, exit!")
        exit(-1)
