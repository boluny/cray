import unittest
import os

from cray.craylib.post import Post

POST_DIR = os.path.join(__file__, "../test_site", "_post")

def get_test_suites():
    '''Return test cases as a suite in this module'''
    suite = unittest.TestSuite()
    suite.addTest(PostGenerateTestCase())

    return suite

class PostGenerateTestCase(unittest.TestCase):
    '''Test case for post generation'''
    def runTest(self):
        '''Run test'''
        p_hello_world = Post(os.path.join(POST_DIR, "2017-06-02-hello-world.markdown"))
        p_non_existence = Post(os.path.join(POST_DIR, "2015-09-18-no-existence.markdown"))

        should_meta = {'title': r'"Welcome to Cray!"',
                       'layout': 'post',
                       'date': '2017-06-02 22:22:22',
                       'categories': 'demo',
                       '__file_name': ['hello', 'world']
                      }
        self.assertFalse(p_non_existence.is_existed())

        self.assertTrue(p_hello_world.is_existed())
        p_hello_world.parse_file()
        p_hello_world_meta = p_hello_world.get_meta()
        self.assertEqual(should_meta, p_hello_world_meta)
