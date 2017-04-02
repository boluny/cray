class Page(object):
    """the frame that shows as pages"""

    def __init__(self, file_name):
        self._file_name = file_name
        self._content = ""

    def get_content(self):
        return self._content


