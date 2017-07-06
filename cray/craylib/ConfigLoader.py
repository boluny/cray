# -*- coding: utf-8 -*-
'''module for configuration loader class'''

import json
import os

# TODO: could adopt singelon pattern
class ConfigLoader(object):

    def __init__(self, root_dir):
        self.__root_dir = root_dir
        self.__config_dict = {}

    def get_config(self):
        return self.__config_dict

    def parse_config(self):
        config_name = os.path.join(self.__root_dir, 'config.json')
        if not os.path.exists(config_name):
            return False

        with open(config_name, 'r', encoding='utf-8') as conf_fp:
            config_content = conf_fp.read().replace('\n', ' ').replace('\r', ' ')

        self.__config_dict = json.loads(config_content)

        if self.__config_dict and isinstance(self.__config_dict, dict):
            return True

        return False
