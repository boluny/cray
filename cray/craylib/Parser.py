# -*- coding: utf-8 -*-
import io

class Parser(object):
    """description of class"""
    def __init__(self, content):
        self.__content = content

    def parse(self):
        meta = dict()
        triple_hyphen = 0
        buf = io.StringIO(self.__content)

        # TODO: optimize the search of metadata start with and end with '---'
        # using regular expression
        line = buf.readline()
        while line is not None:
            if line.startswith('---'):
                triple_hyphen += 1

            if triple_hyphen == 1:
                if not line.startswith('-') and not line.startswith('#'):
                    # let maxsplit set to 1 to just take the first ':' as splitter 
                    attribute_and_value = line.split(':', 1)
                    meta[attribute_and_value[0].strip()] = \
                        attribute_and_value[1].strip()
            elif triple_hyphen == 2:
                # if the second '---\n' is encountered, it means meta part is over
                break

            line = buf.readline()
        
        content = buf.read()
        
        return meta, content

