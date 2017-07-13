# -*- coding: utf-8 -*-
'''
The module of a page object.
'''

import codecs
import os

from cray.craylib import utility
from cray.craylib.Parseable import Parseable


class Page(Parseable):
    """the frame that shows as pages"""

    def __init__(self, file_name):
        '''Create a page object with absolute file name. '''
        super().__init__(file_name)
        self.set_post_process_hook(self.page_post_process)

    def page_post_process(self, fresh_meta):
        '''customized post process logic for page object '''
        pure_file_name = utility.file_name_no_ext(self._file_name)
        # The solution is ugly here but the leading slash mark is needed
        # Call for improvement for this
        self._post_process_meta['url_dir'] = pure_file_name + os.sep
        self._post_process_meta['url'] = os.sep + pure_file_name + os.sep
        self._post_process_meta['content'] = self.get_content()
        self._post_process_meta.update(fresh_meta)

        # trim page.title to get rid of double quotation mark
        if 'title' in self._post_process_meta:
            self._post_process_meta['title'] = \
            utility.trim_quotation_mark(self._post_process_meta['title'])
        else:
            self._post_process_meta['title'] = pure_file_name


    def as_dict(self):
        '''return the metas with some customized post processing'''
        return self._post_process_meta

