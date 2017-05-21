from craylib import Post
from craylib import utility
import os
#from .Post import *

_logger = utility.get_logger('cray.PostManager')

class PostManager(object):
    """The class to manage all the posts in the sites."""
    def __init__(self, post_dir):
        self.__post_dir = post_dir
        self.__posts_list = []
        _logger.debug('post_dir: %s', post_dir)

    def execute(self, params):
        """
        Execute for the specified command e.g. new/list
        """
        
        self.__params = params
        _logger.debug('params: %s', params)

        assert len(self.__params) == 2
        if self.__params[0] == 'read':
            pp = Post.Post(os.path.join(self.__post_dir, self.__params[1]))
            if pp.parse_file() == utility.RT.SUCCESS:
                print(pp.get_metadata())
                print(pp.get_content())               
        

    def create(self, file_name):
        pass

    def delete(self, file_name):
        pass

    def is_post_exist(self, file_name):
        pass

    def set_post_dir(self, path):
        pass

    def get_all_posts(self):
        post_list = []
        files = os.listdir(self.__post_dir)
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                pp = Post.Post(os.path.join(self.__post_dir, file))
                if pp.parse_file() == utility.RT.SUCCESS:
                    post_list.append(pp)

        return post_list
        



