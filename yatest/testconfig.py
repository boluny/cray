# -*- coding: utf-8 -*-
'''test cases for config_loader module'''

import unittest
import os
import cray.craylib.config_loader as config_loader

ROOT_DIR = os.path.join(os.path.dirname(__file__), "test_site")

def get_test_suites():
    '''Return test cases as a suite in this module'''
    suite = unittest.TestSuite()
    suite.addTest(ConfigLoadTestCase())

    return suite

class ConfigLoadTestCase(unittest.TestCase):
    '''Test case for post generation'''
    def runTest(self):
        '''Run test'''
        conf_ld = config_loader.ConfigLoader(ROOT_DIR)
        self.assertTrue(conf_ld.parse_config())
        confs = conf_ld.get_config()
        self.assertTrue('description' in confs)
        self.assertEqual(confs['description'], "demo site description")

        self.assertTrue('title' in confs)
        self.assertEqual(confs['title'], "Demo")

        self.assertTrue('url' in confs)
        self.assertEqual(confs['url'], "www.demo.com")

        self.assertTrue('protocol' in confs)
        self.assertEqual(confs['protocol'], "http")

        self.assertTrue('generate_path' in confs)
        self.assertEqual(confs['generate_path'], "..")

        self.assertFalse('page_number' in confs)
