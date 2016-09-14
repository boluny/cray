from .Post import Post

class PostManager(object):
    """The class to manage all the posts in the sites."""
    def __init__(self, post_dir, params):
        print(post_dir)
        print(params)
        self._post_dir = post_dir
        self._params = params


