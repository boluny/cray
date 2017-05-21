# -*- coding: utf-8 -*-
from craylib import utility
from craylib.Parser import Parser
import os
import codecs

_logger = utility.get_logger('cray.page')

class Page(object):
    """the frame that shows as pages"""

    def __init__(self, file_name):
        self.__file_name = file_name

    def get_content(self):
        return self.__content

    def parse_file(self):
        # TODO: add exception or failture test
        if not self.is_existed():
            _logger.warning("specified file %s does not exist.", self._post_file_name)
            return

        with codecs.open(self.__file_name, 'r', 'utf-8') as post_fd:
            whole_content = post_fd.read()
            pp = Parser(whole_content)
            self.__meta, self.__content = pp.parse()

        _logger.debug("meta: %s", self.__meta)
        _logger.debug("content: %s", self.__content)
        return utility.RT.SUCCESS

    def as_dict(self):
        ret_dict = {}

        pure_file_name = os.path.split(self.__file_name)[1].rpartition('.')[0]
        # The solution is ugly here but the leading slash mark is needed
        # Call for improvement for this 
        ret_dict['url_dir'] = pure_file_name + os.sep
        ret_dict['url'] = os.sep + pure_file_name + os.sep
        ret_dict['content'] = self.__content
        ret_dict.update(self.__meta)

        # trim page.title to get rid of double quotation mark
        if 'title' in ret_dict:
            ret_dict['title'] = utility.trim_quotation_mark(ret_dict['title'])
        else:
            ret_dict['title'] = pure_file_name

        return ret_dict

    def is_existed(self):
        return os.path.exists(self.__file_name)
