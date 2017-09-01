import unittest
import os
import cray.craylib.utility as test_module

ROOT_DIR = os.path.join(os.path.dirname(__file__), "test_site")

def get_test_suites():
    '''Return test cases as a suite in this module'''
    suite = unittest.TestSuite()
    suite.addTest(UtilityIsValidSiteTestCase())

    return suite

class UtilityIsValidSiteTestCase(unittest.TestCase):
    '''Test case for post generation'''
    def runTest(self):
        '''Run test'''
        self.assertTrue(test_module.is_valid_site(ROOT_DIR))
        self.assertFalse(test_module.is_valid_site("test"))
