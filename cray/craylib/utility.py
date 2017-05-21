import os
import logging
import http.server
import socketserver
from enum import Enum

class RT(Enum):
    SUCCESS = 1
    FAILURE = 2
    UNKNOWN = 3


def get_path_splitter():
    return os.sep

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

    PORT = 80

    os.chdir(root_dir)

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    httpd.serve_forever()

def trim_quotation_mark(original_str):
    
    if original_str.startswith('"') and original_str.endswith('"'):
        return original_str[1:-1]
    else:
        return original_str
