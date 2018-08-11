# -*- coding: utf-8 -*-
'''test cases for post_manager module'''

import unittest
import os
from datetime import date

from cray.craylib.post_manager import PostManager

POST_DIR = os.path.join(os.path.dirname(__file__), "test_site", "_post")

def get_test_suites():
    '''Return test cases as a suite in this module'''
    suite = unittest.TestSuite()
    suite.addTest(PostManagerListTestCase())
    suite.addTest(PostManagerReadTestCase())
    suite.addTest(PostManagerCreateDeleteTestCase())

    return suite

class PostManagerListTestCase(unittest.TestCase):
    '''Test case for post manager list command'''
    def runTest(self):
        '''Run test'''
        my_post_manager = PostManager(POST_DIR)
        post_list = my_post_manager.list_all_post()

        self.assertTrue(isinstance(post_list, list))
        self.assertEqual(1, len(post_list))
        self.assertEqual('2017-06-02-hello-world.markdown', post_list[0])


class PostManagerReadTestCase(unittest.TestCase):
    '''Test case for post manager read command'''
    def runTest(self):
        '''Run test'''
        my_post_manager = PostManager(POST_DIR)
        meta, content = my_post_manager.read_post('2017-06-02-hello-world.markdown')
        should_meta = {'title': r'"Welcome to Cray!"',
                       'layout': 'post',
                       'date': '2017-06-02 22:22:22',
                       'category': 'demo',
                       'public': 'true',
                       '__file_name': ['hello', 'world']
                      }
        self.assertEqual(should_meta, meta)
        self.assertRegex(content, '.*hello world!.*')

        meta, content = my_post_manager.read_post('2015-09-18-no-existence.markdown')
        self.assertEqual({}, meta)
        self.assertEqual(content, '')

class PostManagerCreateDeleteTestCase(unittest.TestCase):
    '''Test case for post manager create/delete command'''
    def runTest(self):
        '''Run test'''
        new_file_name = 'test.markdown'
        gen_file_name = str(date.today()) + '-' + new_file_name
        file_path = os.path.join(POST_DIR, gen_file_name)
        my_post_manager = PostManager(POST_DIR)

        self.assertFalse(os.path.exists(file_path))

        my_post_manager.create(new_file_name)
        self.assertTrue(os.path.exists(file_path))

        my_post_manager.delete(gen_file_name)
        self.assertFalse(os.path.exists(file_path))
