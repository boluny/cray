class Post(object):
    """description of class"""
    def __init__(self, filename):
        self._post_meta_data = {}
        self._post_content = ""
        self._post_file_name = filename

    def get_content(self):
        return self._post_content

    def get_metadata(self):
        return self._post_meta_data

    def parse_file(self):
        pass
