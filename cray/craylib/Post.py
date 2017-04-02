from craylib import utility
import os

_logger = utility.get_logger('cray.post')

class Post(object):
    """description of class"""
    def __init__(self, filename):
        self._post_meta_data = {}
        self._post_content = ""
        self._post_file_name = filename
        _logger.debug("receive file name: " + filename)

    def get_content(self):
        return self._post_content

    def get_metadata(self):
        return self._post_meta_data

    def parse_file(self):

        # TODO: add exception or failture test
        if not self.is_existed():
            _logger.warning("specified file %s does not exist.", self._post_file_name)
            return
        triple_hyphen = 0 
        with open(self._post_file_name, 'r') as post_fd:
            line = post_fd.readline()
            while line is not None:
                if line.startswith('---'):
                    triple_hyphen += 1

                if triple_hyphen == 1:
                    if not line.startswith('-') and not line.startswith('#'):
                        # let maxsplit set to 1 to just take the first ':' as splitter 
                        attribute_and_value = line.split(':', 1)
                        self._post_meta_data[attribute_and_value[0].strip()] = \
                            attribute_and_value[1].strip()
                elif triple_hyphen == 2:
                    # if the second '---\n' is encountered, it means meta part is over
                    break

                line = post_fd.readline()

            self._post_content = post_fd.read()
        _logger.debug("meta: %s", self._post_meta_data)
        _logger.debug("content: %s", self._post_content)
        return utility.RT.SUCCESS
        

    def is_existed(self):
        return os.path.exists(self._post_file_name)
