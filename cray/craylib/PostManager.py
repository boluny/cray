from craylib import Post
from craylib import utility
import os
#from .Post import *

_logger = utility.get_logger('cray.PostManager')

class PostManager(object):
    """The class to manage all the posts in the sites."""
    def __init__(self, post_dir, params):
        self._post_dir = post_dir
        self._params = params
        self._posts_list = []
        _logger.debug('post_dir: %s, params: %s', post_dir, params)

        assert len(self._params) == 2
        if self._params[0] == 'read':
            pp = Post.Post(os.path.join(self._post_dir, self._params[1]))
            if pp.parse_file() == utility.RT.SUCCESS:
                print(pp.get_metadata())
                print(pp.get_content())
                self._posts_list.append(pp)

    def execute(self):
        """
        Execute for the specified command e.g. new/list
        """
        pass

    def create(self, file_name):
        pass

    def delete(self, file_name):
        pass

    def is_post_exist(self, file_name):
        pass

    def set_post_dir(self, path):
        pass

    def get_all_posts(self):
        pass



