from sys import argv
from jinja2 import Template
from craylib.PostManager import PostManager

import os

TEST_SITE = 'sample_site'
POST_DIR = '_post'
THEME_DIR = '_theme'
FRAME_DIR = '_frame'
GENERATED_SITE_DIR = '_site'

if __name__ == '__main__':
    if len(argv) <= 2:
        print("Arguments are not sufficient")
        exit(-1)

    print(argv)
    print(os.path.join(os.getcwd(), TEST_SITE, POST_DIR))

    # handle post related command logic
    if argv[1] == 'post':

        posts_dir = os.path.join(os.getcwd(), TEST_SITE, POST_DIR)
        pm = PostManager(posts_dir, argv[2:])
        
    elif argv[1] == 'frame':
        pass
    elif argv[1] == 'generate':
        pass
    elif argv[1] == 'test':
        pass
    elif argv[1] == 'deploy':
        pass
    else:
        print("Unimplemented option, exit!")
        exit(-1)
