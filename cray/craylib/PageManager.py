import os
from craylib.Page import Page
from craylib import utility

_logger = utility.get_logger('cray.PageManager')

class PageManager(object):
    """Manager of pages"""
    _init_template = ""

    def __init__(self, page_dir):
        self.__cmd_params = 'transient'
        self.__page_dir = page_dir
        _logger.debug('page_dir: %s', page_dir)

    def create(self, file_name):
        pass

    def delete(self, file_name):
        pass

    def is_exist(self, file_name):
        pass

    def set_page_dir(self, path):
        pass

    def get_all_pages(self):
        page_list = []
        files = os.listdir(self.__page_dir)
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                pp = Page(os.path.join(self.__page_dir, file))
                if pp.parse_file() == utility.RT.SUCCESS:
                    page_list.append(pp.as_dict())

        return page_list

