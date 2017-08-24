import unittest
import os

from cray.craylib.page import Page

PAGE_DIR = os.path.join(os.path.dirname(__file__), "test_site", "_page")

def get_test_suites():
    '''Return test cases as a suite in this module'''
    suite = unittest.TestSuite()
    suite.addTest(PageGenerateTestCase())

    return suite

class PageGenerateTestCase(unittest.TestCase):
    '''Test case for page generation'''
    def runTest(self):
        '''Run test'''
        p_about = Page(os.path.join(PAGE_DIR, "about.md"))
        p_non_existence = Page(os.path.join(PAGE_DIR, "no-existence.markdown"))

        should_meta = {'title': r'about',
                       'layout': 'page',
                       'permalink': '/about/'
                      }
        self.assertFalse(p_non_existence.is_existed())

        self.assertTrue(p_about.is_existed())
        p_about.parse_file()
        p_about_meta = p_about.get_meta()
        self.assertEqual(should_meta, p_about_meta)
