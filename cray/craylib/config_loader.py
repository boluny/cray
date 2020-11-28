# -*- coding: utf-8 -*-
'''module for configuration loader class'''

# Not using yaml is due to the laziness of the author who don't want to import extra dependency.

import json
import os


# TODO: could adopt singelon pattern
class ConfigLoader(object):
    '''Class for load the site configuration'''
    def __init__(self, root_dir):
        self.__root_dir = root_dir
        self.__config_dict = {}

    def get_config(self):
        '''Return the configuration pair in dictionary'''
        return self.__config_dict

    def parse_config(self):
        '''Parse site configuration file in json'''
        config_name = os.path.join(self.__root_dir, 'config.json')
        if not os.path.exists(config_name):
            return False

        trim_json_lines = []

        with open(config_name, 'r', encoding='utf-8') as conf_fp:
            config_content = conf_fp.readlines()
            # Add support for comment style like //
            for line in config_content:
                trim_json_lines.append(line[:line.find('//')])

            final_conf = ' '.join(trim_json_lines).replace('\n', ' ').replace('\r', ' ')

        self.__config_dict = json.loads(final_conf)

        if self.__config_dict and isinstance(self.__config_dict, dict):
            return True

        return False
