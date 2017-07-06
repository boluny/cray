# -*- coding: utf-8 -*-
'''miscellaneous tools which can't be classified'''

import os
import logging
import http.server
import socketserver
from enum import Enum

TEST_SITE = 'sample_site'
POST_DIR = '_post'
PAGE_DIR = '_page'
THEME_DIR = '_theme'
GENERATED_SITE_DIR = '_site'

class RT(Enum):
    SUCCESS = 1
    FAILURE = 2
    UNKNOWN = 3

def is_valid_site(root_dir):
    '''Check if the site contains sub directories '_post', '_page', '_theme'''
    post_dir = os.path.join(root_dir, '_post')
    page_dir = os.path.join(root_dir, '_page')
    theme_dir = os.path.join(root_dir, '_theme')
    config_file = os.path.join(root_dir, 'config.json')

    if os.path.exists(post_dir) and os.path.exists(page_dir) and os.path.exists(theme_dir) \
    and os.path.exists(config_file):
        return True

    return False

def get_logger(name):
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Copy following from https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger

def start_server(root_dir):

    HTTP_PORT = 80

    os.chdir(root_dir)

    handler_alias = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", HTTP_PORT), handler_alias)
    print("serving at 127.0.0.1:%d" % HTTP_PORT)
    httpd.serve_forever()

def trim_quotation_mark(original_str):
    '''Remove the quotation at leading and last position'''
    if original_str.startswith('"') and original_str.endswith('"'):
        return original_str[1:-1]
    else:
        return original_str

def full_generate_path(root, conf_dict):
    
    generate_path = conf_dict['generate_path'] if 'generate_path' in conf_dict else '.'
    site_name = conf_dict['site_name'] if 'site_name' in conf_dict else '_site'
    return os.path.join(root, generate_path, site_name)
    
