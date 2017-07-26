# -*- coding: utf-8 -*-
'''miscellaneous tools which can't be classified'''

import os
import logging
import http.server
import socketserver
import shutil
from enum import Enum

TEST_SITE = 'sample_site'
POST_DIR = '_post'
PAGE_DIR = '_page'
THEME_DIR = '_theme'
GENERATED_SITE_DIR = '_site'

class RT(Enum):
    '''Representation for return value, deprecate it is in consideration'''
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
    '''Return a logger for debug/log stuff'''
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Copy following from https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial
    # create console handler and set level to debug
    my_sm_handler = logging.StreamHandler()
    my_sm_handler.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d - \
    %(levelname)s - %(message)s')

    # add formatter to ch
    my_sm_handler.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(my_sm_handler)

    return logger

def start_server(root_dir):
    '''start the server in the directory specified by function argument.
    root_dir:string the absolute path of a directory.
    '''
    HTTP_PORT = 80

    os.chdir(root_dir)

    handler_alias = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", HTTP_PORT), handler_alias)
    print("serving at 127.0.0.1:%d" % HTTP_PORT)
    httpd.serve_forever()

def trim_double_quotation_mark(original_str):
    '''Remove the double quotation at leading and last position'''
    if original_str.startswith('"') and original_str.endswith('"'):
        return original_str[1:-1]

    return original_str

def full_generate_path(root, conf_dict):
    '''Return the absolute path when configured "generate_path" in configuration file,
    else using the default directory name "_site"
    '''
    generate_path = conf_dict['generate_path'] if 'generate_path' in conf_dict else '.'
    site_name = conf_dict['site_name'] if 'site_name' in conf_dict else '_site'
    return os.path.join(root, generate_path, site_name)

def copy_subdir(root_dir, subdirs, dest_dir):
    '''Copy subdirectories from source directory to destination directory
    :param root_dir: The source directory
    :param subdires: List of subdirectories names in root_dir
    :param dest_dir: The destination directory
    :returns: None
    '''
    if not root_dir or not subdirs or not dest_dir:
        return

    for sub in subdirs:
        sub_abs_path = os.path.join(root_dir, sub)
        dest_sub_abs_path = os.path.join(dest_dir, sub)
        if os.path.exists(sub_abs_path):
            shutil.copytree(sub_abs_path, dest_sub_abs_path)

def name_conflict(src_str_list, dest_str_list):
    '''Check if the same element in the src_str_list and dest_str_list'''
    return any([a_str in dest_str_list for a_str in src_str_list])

def file_name_no_ext(file_name):
    '''Get the filename without its extension'''
    return os.path.split(file_name)[1].rpartition('.')[0]
