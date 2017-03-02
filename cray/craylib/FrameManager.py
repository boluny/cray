from .Frame import Frame

class FrameManager(object):
    """Manager of Frames"""
    _init_template = ""

    def __init__(self, cmd_params, frame_dir):
        self._frame_list = []
        self._cmd_params = cmd_params
        self._frame_dir = frame_dir

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

