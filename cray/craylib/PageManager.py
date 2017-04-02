from craylib.Page import Page

class PageManager(object):
    """Manager of pages"""
    _init_template = ""

    def __init__(self, cmd_params, frame_dir):
        self._page_list = []
        self._cmd_params = cmd_params
        self._page_dir = frame_dir

    def create(self, file_name):
        pass

    def delete(self, file_name):
        pass

    def is_exist(self, file_name):
        pass

    def set_frame_dir(self, path):
        pass

    def get_all_frames(self):
        pass

